import sys
import os

# Add parent directory to path to import BaseTool if running from 'tools/'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from base_tool import BaseTool
except ImportError:
    # Fallback if base_tool is in a specific package structure
    from lm_studio_client.base_tool import BaseTool

class CalculatorTool(BaseTool):
    @property
    def name(self):
        return "calculator"

    @property
    def description(self):
        return "Useful for performing math calculations. Input should be a mathematical expression string like '2 + 2'."

    def get_parameters(self):
        """
        Returns the JSON Schema for the tool's parameters.
        """
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to evaluate (e.g., '2 + 2', '5 * 10')"
                }
            },
            "required": ["expression"]
        }

    def execute(self, expression):
        """
        Executes the calculation.
        
        Args:
            expression (str): The mathematical expression to evaluate.
        """
        try:
            # Clean the expression
            clean_expression = str(expression).strip().replace("`", "").replace("python", "")
            
            # Allow basic math functions
            allowed_names = {
                "abs": abs, "round": round, "min": min, "max": max, "pow": pow,
                "sum": sum
            }
            
            # SAFEGUARD: In production, use AST parsing or a library like `simpleeval`.
            # For this test, eval is used with limited globals.
            result = eval(clean_expression, {"__builtins__": {}}, allowed_names)
            
            return str(result)
        except Exception as e:
            return f"Error calculating '{expression}': {str(e)}"