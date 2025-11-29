import os 
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

def main():
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

    if len(sys.argv) - 1 == 0:
        print("Prompt is missing.  Exiting program.")
        sys.exit(1)

    # convert sys.argv list to a single string, excluding the app name
    user_prompt = " ".join(sys.argv[1:])
    
    # capture command argument if one was passed; assumes 3rd position
    if (any("--" in x for x in sys.argv[1:])):
        command_prompt = sys.argv[2]
    else:
        command_prompt = ''
    
    welcome_message = "Hello from ai-agent-python!"

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        print("the key variable is empty")

    client = genai.Client(api_key=api_key)
    model_name = 'gemini-2.0-flash-001'

    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config = types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
        )
    )

    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name }({function_call.args})")
    else:
        print(response.text)
        
    sys.exit(0)

if __name__ == "__main__":
    main()
