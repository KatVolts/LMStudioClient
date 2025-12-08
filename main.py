from LMStudioClient import *
import json
if __name__ == "__main__":
    # Define Tool
    weather_tool = {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                },
                "required": ["city"]
            }
        }
    }

    # Define function
    def get_weather(city):
        return json.dumps({"city": city, "temp": "24C", "condition": "Sunny"})

    client = LMStudioClient()
    history = []

    print("User: What is the weather in Tokyo?")
    
    # 1. First Turn: Standard Query
    response = client.query(
        "What is the weather in Tokyo?", 
        history=history,
        tools=[weather_tool]
    )

    if isinstance(response, list):
        print(f"[!] Tool Requested: {response[0].function.name}")
        
        # 2. Handle Tool Execution
        for tool_call in response:
            args = json.loads(tool_call.function.arguments)
            result = get_weather(**args)
            
            # Append Tool Result Manually
            history.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

        # 3. Final Turn: CRITICAL CHANGE HERE
        # We pass prompt=None. We do NOT add a new user message.
        # We just want the assistant to see the tool result and finish.
        final_answer = client.query(
            prompt=None,  # <--- No new user text
            history=history,
            tools=[weather_tool]
        )
        print(f"AI: {final_answer}")
    else:
        print(f"AI: {response}")