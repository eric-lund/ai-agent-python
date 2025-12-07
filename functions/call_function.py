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
    function_name = function_call_part.name
    arguments = function_call_part.args
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    target_function = function_map[function_name]
    result = target_function(**working_directory, **arguments)




    # if function_call_part.name == 'get_files_info':
    #     results = get_files_info(**working_directory)
    # elif function_call_part.name == "get_file_content":
    #     results = get_file_content(**working_directory, **arguments)
    # elif function_call_part.name == 'write_file':
    #     results = write_file(**working_directory, **arguments)
    # elif function_call_part.name == 'run_python_file':
    #     results = run_python_file(**working_directory, **arguments)

    print(results)
    

