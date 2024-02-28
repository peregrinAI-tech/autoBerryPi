import autogen
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
import openai
import yfinance as yf
import os 
from dotenv import load_dotenv
import display_in_waveshare2_fixed as screen
import time
load_dotenv()
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
less_costly_config_list = [{'model': 'gpt-3.5-turbo', 'api_key': os.getenv("OPENAI_API_KEY")},]
config_list = [{'model': 'gpt-4', 'api_key': os.getenv("OPENAI_API_KEY")},]


llm_config_for_manager = {
    "seed": 42,  # seed for caching and reproducibility
    "config_list": config_list,  # a list of OpenAI API configurations
    "temperature": 0,  # temperature for sampling
}



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





name_to_account_id = {
    "Alice": "A123",
    "Bob": "B456",
    "Charlie": "C789"
}

account_id_to_bill = {
    "A123": 120.50,
    "B456": 200.75,
    "C789": 99.99
}

def get_account_id(name):
    return name_to_account_id.get(name, "Name not found")

def get_last_bill_amount(account_id):
    return account_id_to_bill.get(account_id, "Account ID not found")

def get_stock_price(symbol: str) -> float:
    stock = yf.Ticker(symbol)
    price = stock.history(period="1d")['Close'].iloc[-1]
    return price

def display_message(message: str) -> str:
    #print(message)
    screen.draw_text(message)
    #time.sleep(10)
    return "finished sending data"





llm_config = {
    "config_list": less_costly_config_list,
    "seed": 42,
    "functions":[
        {
            "name": "get_account_id",
            "description": "retrieves the account id for a user given their name",
            "parameters": {
                "type": "object",
                "properties": {
                    "name":{
                        "type": "string",
                        "description": "The name of the customer that will be used to lookup the account id"
                    }
                },
                "required":["name"]
            }
        },
        {
            "name": "get_last_bill_amount",
            "description": "Retrieves the last bill amount for a user for a given account id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "account_id":{
                        "type": "string",
                        "description": "The account id fetched from get_account_id that will be used to lookup the last bill for the customer"
                    }
                },
                "required":["account_id"]
            }
        }
    ]
}

billing_assistant_agent_prompt = '''
This agent is a helpful assistant that can retrieve the account id and the last bill amount for a customer. 
Any other customer care requests are outside the scope of this agent. 
Once you have completed assisting the user output TERMINATE'''

billing_assistant_agent = autogen.AssistantAgent(
    name="billing_assistant_agent",
    system_message=billing_assistant_agent_prompt,
    llm_config=llm_config,
)


function_executor_agent_prompt = '''
This agent executes all functions for the group. 
Anytime an agent needs information they will prompt this agent with the indicated function and arguments.
'''
function_executor_agent = autogen.AssistantAgent(
    name="function_executor_agent",
    system_message=function_executor_agent_prompt,
    llm_config=llm_config ,
)
function_executor_agent.register_function(
    function_map={
        "get_account_id": get_account_id,
        "get_last_bill_amount": get_last_bill_amount,
    }
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "CHatOut",
        "use_docker": False,  # Opcional
    },
)


groupchat = autogen.GroupChat(agents=[user_proxy, billing_assistant_agent, function_executor_agent], messages=[], max_round=50)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config_for_manager,code_execution_config={"use_docker": False})


user_proxy.initiate_chat(manager, message="Hello!")

