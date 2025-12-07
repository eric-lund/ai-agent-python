from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    working_directory = {"working_directory": "./calculator"}
    arguments = (function_call_part.args)

    if function_call_part.name == 'get_files_info':
        results = get_files_info(**working_directory)
    elif function_call_part.name == "get_file_content":
        results = get_file_content(**working_directory, **arguments) 

    print(results)
    

