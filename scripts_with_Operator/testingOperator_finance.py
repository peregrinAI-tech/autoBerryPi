import autogen
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
import openai
import yfinance as yf
import os 
from dotenv import load_dotenv
import display_in_waveshare2_fixed as screen
import time
# Load the environment variables from the .env file
load_dotenv()





client = openai.OpenAI()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_stock_price(symbol: str) -> float:
    stock = yf.Ticker(symbol)
    price = stock.history(period="1d")['Close'].iloc[-1]
    return price

def display_message(message: str) -> str:
    #print(message)
    operatorMessage = f"Operator Here:{message} "  
    screen.draw_text(operatorMessage)
    #time.sleep(10)
    return "finished sending data"

#lala = display_message("Aqui empezamos , quihubo")

tools_list = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Retrieve the latest closing price of a stock.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The ticker symbol of the stock."
                    }
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "display_message",
            "description": "Display a given text message into a terminal.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "The text message to display."
                    }
                },
                "required": ["message"]
            }
        }
    }
]



llm_config = { 
    "tools": tools_list,
}
gpt_assistant = GPTAssistantAgent(
    name="Stock Assistant",
    instructions="""
    You are a Stock Expert.You search for stock values and communicate your actions and findings to scribe.
    Reply TERMINATE when the task is solved and there is no problem.
    """,
    llm_config=llm_config,
    code_execution_config=False
)

scribe_assistant = GPTAssistantAgent(
    name="Scribe Assistant",
    instructions="""
    You are a scribe. 
    You communicate with the other agents about their actions and use the terminal (function given) to send 
    short messages of status and actions from other assistants
    """,
    llm_config=llm_config,
    code_execution_config=False
)

scribe_assistant.register_function(
    function_map={
        "display_message": display_message,
    }
)



gpt_assistant.register_function(
    function_map={
        "display_message": display_message,
        "get_stock_price": get_stock_price,
    }
)


user_proxy = autogen.UserProxyAgent(
    name="Mr. Pilgrim",
    code_execution_config={
        "work_dir": "financeOut",
        "use_docker": False,  # Opcional
    },
)

user_proxy.initiate_chat(
    gpt_assistant,
    scribe_assistant,
    message="""
    Please tell me the latest value for stock exchave for CEMEX
    """
)
