import os
import sys
import json
import importlib.util
import inspect
from typing import List

# Internal Imports
from lm_studio_client import LMStudioClient
from base_tool import BaseTool
from tool_loader import ToolLoader


if __name__ == "__main__":
    # 1. Initialize Client
    client = LMStudioClient()
    history = []
    
    # 2. Load Tools
    print("--- Initializing ---")
    TL = ToolLoader()
    print(f"Tools available: {list(TL.tool_registry.keys())}")
    # 3. Define the Prompt
    user_input = "Hello. How are you?"
    print(f"User: {user_input}")

    # 4. First Query
    response = client.query(
        user_input, 
        history=history, 
        tools=TL.tool_definitions if TL.tool_definitions else None
    )

    # 5. Handle Tool Usage
    if isinstance(response, list):
        print(f"[!] Model requested {len(response)} tool call(s).")
        
        for tool_call in response:
            func_name = tool_call.function.name
            
            if func_name in TL.tool_registry:
                # Parse Args
                args = json.loads(tool_call.function.arguments)
                print(f"    Executing '{func_name}' with args: {args}")
                
                # Execute Logic
                tool_instance = TL.tool_registry[func_name]
                result_json = tool_instance.execute(**args)
                print(f"Tool result {result_json}")
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
            tools=TL.tool_definitions
        )
        print(f"AI: {final_answer}")
    
    else:
        # Standard Text Response
        print(f"AI: {response}")