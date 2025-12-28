from functions.config import SYSTEM_PROMPT, MODEL_NAME
from google.genai import types

def call_llm(messages: list, tools: dict, client: str):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=messages,
        config = types.GenerateContentConfig(
            tools=[tools], 
            system_instruction=SYSTEM_PROMPT
        )
    )

    return response
