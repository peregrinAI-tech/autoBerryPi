from autogen import AssistantAgent, UserProxyAgent, config_list_from_json, GroupChat, GroupChatManager
from dotenv import load_dotenv
import os
import display_in_waveshare2_fixed as screen

# Load the environment variables from the .env file
load_dotenv()



less_costly_config_list = [{'model': 'gpt-3.5-turbo', 'api_key': os.getenv("OPENAI_API_KEY")},]
config_list = [{'model': 'gpt-4', 'api_key': os.getenv("OPENAI_API_KEY")},]


llm_config_for_manager = {
    "seed": 42,  # seed for caching and reproducibility
    "config_list": config_list,  # a list of OpenAI API configurations
    "temperature": 0,  # temperature for sampling
}


llm_config = {
    "functions": [
        
        {
            "name": "display_message",
            "description": "Display a text message in the console.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Text message to display in the console.",
                    }
                },
                "required": ["message"],
            },
        },
        {
            "name": "sh",
            "description": "run a shell script and return the execution result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "script": {
                        "type": "string",
                        "description": "Valid shell script to execute.",
                    }
                },
                "required": ["script"],
            },
        },
    ],
    "config_list": less_costly_config_list,
    "timeout": 120,
    "temperature": 0,  # temperature for sampling
    "seed": 42
}


# create an AssistantAgent named "assistant"
assistant = AssistantAgent(
    name="assistant",
    system_message = '''You are an assistant that creates a plan based on the request and approves dictates what 
should be done next, you communicate all your actions to the operator and then proceed implementing ''',
    max_consecutive_auto_reply=2,
    llm_config=llm_config,  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False, }
)

operator = AssistantAgent(
    name="operator",
    system_message=''' You are a scribe that transmits short messages to a terminal 
trough the corresponding function. The messages involve short descriptions of the decisions taken by the Assistant
as well resumed plans executed by the user proxy.For coding tasks, only use the function display_message.''',
    llm_config=llm_config,  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
)



# Configura el UserProxyAgent con esta lógica
user_proxy = UserProxyAgent(
    name="user_proxy",
    #human_input_mode="ALWAYS",  # Pide la entrada del usuario después de cada respuesta automática
    #max_consecutive_auto_reply=2,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # Opcional
    },
)




def exec_sh(script):
    return user_proxy.execute_code_blocks([("sh", script)])

def display_text(message):
    screen.draw_text(message)


# register the functions
operator.register_function(
    function_map={
        "sh": exec_sh,
        "display_message": display_text,
    }
)

groupchat = GroupChat(agents=[user_proxy, assistant,operator], messages=[], max_round=10)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config_for_manager, code_execution_config={"use_docker": False})

user_proxy.initiate_chat(manager, message='''Check for the contents of your root folder with ls command''')

#user_proxy.initiate_chat(user_proxy,assistant, message=''' Crewate code to display the first 52 digits in the PI number''')

# the assistant receives a message from the user_proxy, which contains the task description



