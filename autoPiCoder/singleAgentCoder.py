from autogen import AssistantAgent, UserProxyAgent, config_list_from_json, GroupChat, GroupChatManager
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()




config_list = [{'model': 'gpt-4', 'api_key': os.getenv("OPENAI_API_KEY")},]


llm_config = {
    "seed": 42,  # seed for caching and reproducibility
    "config_list": config_list,  # a list of OpenAI API configurations
    "temperature": 0,  # temperature for sampling
}



# create an AssistantAgent named "assistant"
assistant = AssistantAgent(
    name="assistant",
    llm_config=llm_config,  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
)


# Configura el UserProxyAgent con esta lógica
user_proxy = UserProxyAgent(
    name="user_proxy",
    #human_input_mode="ALWAYS",  # Pide la entrada del usuario después de cada respuesta automática
    max_consecutive_auto_reply=3,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,  # Opcional
    },
)




# the assistant receives a message from the user_proxy, which contains the task description
user_proxy.initiate_chat(
    assistant,
    message = '''You are a highly skilled expert in Bash scripting and Linux system administration, 
with a particular talent for working with Raspberry Pi devices. Your expertise extends to seamlessly 
installing critical modules and software packages on Raspberry Pi systems. Moreover, you possess a 
keen ability to troubleshoot and resolve coding errors efficiently. Additionally, you excel in 
configuring Raspberry Pi systems to meet and exceed user interaction expectations, ensuring an 
optimized and user-friendly experience.''')
