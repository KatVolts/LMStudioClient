import os
import sys
import json
import importlib.util
import inspect
from typing import List

# Internal Imports
from lm_studio_client import LMStudioClient
from base_tool import BaseTool

def load_tools_from_directory(directory: str) -> List[BaseTool]:
    """
    Dynamically imports .py files from 'directory' and returns instances
    of classes inheriting from BaseTool.
    """
    loaded_tools = []
    
    if not os.path.exists(directory):
        print(f"Warning: Tool directory '{directory}' not found.")
        return []

    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename != "__init__.py":
            file_path = os.path.join(directory, filename)
            module_name = filename[:-3]

            try:
                # Load module definition
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)

                    # Scan for Tool classes
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        # Must inherit BaseTool, but not BE BaseTool
                        if issubclass(obj, BaseTool) and obj is not BaseTool:
                            print(f"   -> Loaded: {name}")
                            loaded_tools.append(obj())
            except Exception as e:
                print(f"Error loading {filename}: {e}")

    return loaded_tools

if __name__ == "__main__":
    # 1. Initialize Client
    client = LMStudioClient()
    history = []
    
    # 2. Load Tools
    print("--- Initializing ---")
    tools_list = load_tools_from_directory("tools")
    
    # Map names to instances for execution
    tool_registry = {t.name: t for t in tools_list}
    # Create JSON definitions for the LLM
    tool_definitions = [t.to_definition() for t in tools_list]

    print(f"Tools available: {list(tool_registry.keys())}")
    print("-" * 30)

    # 3. Define the Prompt
    user_input = "What is the weather in Tokyo?"
    print(f"User: {user_input}")

    # 4. First Query
    response = client.query(
        user_input, 
        history=history, 
        tools=tool_definitions if tool_definitions else None
    )

    # 5. Handle Tool Usage
    if isinstance(response, list):
        print(f"[!] Model requested {len(response)} tool call(s).")
        
        for tool_call in response:
            func_name = tool_call.function.name
            
            if func_name in tool_registry:
                # Parse Args
                args = json.loads(tool_call.function.arguments)
                print(f"    Executing '{func_name}' with args: {args}")
                
                # Execute Logic
                tool_instance = tool_registry[func_name]
                result_json = tool_instance.execute(**args)
                
                # Add Result to History
                history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result_json
                })
            else:
                print(f"    Error: Unknown tool '{func_name}'")

        # 6. Follow-up Query (Send tool results back to model)
        # We pass prompt=None so the model generates immediately based on history
        final_answer = client.query(
            prompt=None, 
            history=history,
            tools=tool_definitions
        )
        print(f"AI: {final_answer}")
    
    else:
        # Standard Text Response
        print(f"AI: {response}")