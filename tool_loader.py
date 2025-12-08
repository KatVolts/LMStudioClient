from base_tool import BaseTool
from typing import List
import os, sys
import inspect
import importlib.util

class ToolLoader():
    def __init__(self, base_url="http://localhost:1234/v1", api_key="lm-studio"):
        self.loadedTools = self.load_tools_from_directory("tools")

    def load_tools_from_directory(self, directory: str) -> List[BaseTool]:
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