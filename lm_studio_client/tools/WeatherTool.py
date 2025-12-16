import json
from base_tool import BaseTool  # Assumes run from root

class WeatherTool(BaseTool):
    name = "get_weather"
    description = "Get current weather for a specific city."

    def get_parameters(self):
        return {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The city name"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["city"]
        }

    def execute(self, city, unit="celsius"):
        # Mock logic
        return json.dumps({
            "city": city,
            "temp": "75" if unit == "fahrenheit" else "24",
            "unit": unit,
            "condition": "Partly Cloudy"
        })