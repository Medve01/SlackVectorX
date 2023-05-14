import openai
from config import Config

config = Config()
openai.api_key=config.get("OPENAI_API_KEY")

def generate_response(conversation):
    messages = prepare_messages(conversation)
    response = openai.ChatCompletion.create(
        model=config.get("OPENAI_MODEL"),
        messages=messages
    )
    return response.choices[0].message.content

def prepare_messages(conversation):
    system_prompt = config.get("GPT_SYSTEM_PROMPT")
    system_prompt+=" The user you are talking to is {}.\n".format(conversation['user_name'].capitalize())

    messages = [{'role': 'system', 'content': system_prompt}]
    messages.extend(conversation['conversation'])
    return messages
