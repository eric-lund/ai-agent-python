import os 
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content
from functions.call_function import call_function


def main():
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_run_python_file,
        schema_get_file_content
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

    print(f'user prompt: {user_prompt}')
    print(f'command prompt: {command_prompt}')

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        print("The key variable is empty")

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

    # Make sure we get a valid response
    if response.usage_metadata is None:
        return print(f'The Gemini API call failed.')
    
    print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
    print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

    if command_prompt == '--verbose':
        verbose = True

    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)
    else:
        print(response.text)
           
    if not function_call_result.parts:
        raise Exception("Missing function call parts.")
    
    if not isinstance(function_call_result.parts[0].function_response, types.FunctionResponse):
        raise Exception("Missing FunctionReponse object.")
    
    if not function_call_result.parts[0].function_response.response:
        raise Exception("Missing response")
    
    function_results = []
    function_results += function_call_result.parts[0]

    if command_prompt:
        print(f"-> {function_call_result.parts[0].function_response.response}")

    sys.exit(0)

if __name__ == "__main__":
    main()
