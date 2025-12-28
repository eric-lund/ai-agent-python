import os 
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.config import GEMINI_API_KEY, DEBUG_TOKENS
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content
from functions.call_function import call_function
from functions.call_llm import call_llm


def main():

    available_functions = dict(types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file,
            schema_run_python_file,
            schema_get_file_content
        ]
    ))

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

    verbose = False
    if command_prompt == '--verbose':
        verbose = True
    
    # print(f'user prompt: {user_prompt}')
    # print(f'command prompt: {command_prompt}')

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    load_dotenv()
    api_key = os.environ.get(GEMINI_API_KEY)

    if api_key is None:
        print("The key variable is empty")

    client = genai.Client(api_key=api_key)
    function_results = []

    # limit model to 20 iterations
    for _ in range(20):
        response = call_llm(messages, available_functions, client)

        # Make sure we get a valid response
        if response.usage_metadata is None:
            return print(f'The Gemini API call failed.')
 
        # Keep a history of responses from the LLM
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if DEBUG_TOKENS:
            print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
            print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose)
        else:
            # Print the final response and leave the loop
            print(response.text)
            break
           
        if not function_call_result.parts:
            raise Exception("Missing function call parts.")
        
        if not isinstance(function_call_result.parts[0].function_response, types.FunctionResponse):
            raise Exception("Missing FunctionReponse object.")
        
        if not function_call_result.parts[0].function_response.response:
            raise Exception("Missing response")
        
        function_results.append(function_call_result.parts[0])
        
        # is this appending the full function_results list??
        messages.append(types.Content(role="user", parts=function_results)),

        # verbose message
        if command_prompt:
            print(f"-> {function_call_result.parts[0].function_response.response}")

    # fail out of the program if the LLM hasn't produced a final response
    if response.function_calls:
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
