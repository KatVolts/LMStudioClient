Based on the file structure and the typical architecture of such tools, here is a complete `README.md` file you can use for the repository.

***

# LMStudioClient

**LMStudioClient** is a modular Python client designed to interact with [LM Studio's](https://lmstudio.ai/) local server. It provides a structured way to build agentic applications by wrapping LLM API calls and offering a native interface for **tool usage** (function calling).

## 🚀 Features

*   **Easy Integration**: Connects seamlessly to LM Studio's local inference server (default: `http://localhost:1234/v1`).
*   **Tool/Function Calling**: Includes a `BaseTool` system to create custom tools that your LLM can execute.
*   **Modular Design**: Separates client logic (`BaseClient`) from implementation (`LMStudioClient`), making it easy to extend.
*   **Agent-Ready**: Designed to facilitate building local AI agents that can interact with their environment.

## 📂 Project Structure

*   `main.py`: The entry point for running the client or testing the agent loop.
*   `lm_studio_client.py`: The core client implementation specific to LM Studio's API.
*   `base_client.py`: Abstract base class defining the standard interface for LLM interaction.
*   `base_tool.py`: Base class for defining custom tools/functions.
*   `tools/`: Directory containing specific tool implementations.

## 🛠️ Prerequisites

1.  **LM Studio**: Download and install [LM Studio](https://lmstudio.ai/).
2.  **Local Server**: Open LM Studio, load a model, and start the **Local Server** (typically on port `1234`).
3.  **Python 3.8+**

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/KatVolts/LMStudioClient.git
cd LMStudioClient
```

Install dependencies (assuming a `requirements.txt` exists, otherwise install `requests` or `openai`):

```bash
pip install requests openai
```

## 💻 Usage

### 1. Basic Chat

You can use the client to send simple prompts to your local model.

```python
from lm_studio_client import LMStudioClient

# Initialize the client (points to localhost:1234 by default)
client = LMStudioClient(base_url="http://localhost:1234/v1")

# Send a message
response = client.chat("What is the capital of France?")
print(response)
```

### 2. Creating & Using Tools

The power of this library lies in its tool support. You can define a new tool by inheriting from `BaseTool`.

**Define a Tool (`tools/my_tool.py`):**

```python
from base_tool import BaseTool

class CalculatorTool(BaseTool):
    def __init__(self):
        super().__init__(name="calculator", description="Useful for performing math calculations.")

    def run(self, expression):
        # specific logic for the tool
        return eval(expression)
```

**Run the Agent (`main.py`):**

```python
from lm_studio_client import LMStudioClient
from tools.my_tool import CalculatorTool

def main():
    # 1. Setup Client
    client = LMStudioClient()

    # 2. Register Tools
    calc_tool = CalculatorTool()
    client.register_tool(calc_tool)

    # 3. Chat with Tool support
    user_input = "What is 25 * 4?"
    
    # The client handles the tool selection and execution automatically (logic depends on implementation)
    response = client.chat_with_tools(user_input)
    
    print(f"Agent: {response}")

if __name__ == "__main__":
    main()
```
