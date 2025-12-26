from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def call_function(function_call, verbose=False):

    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    function_name = function_call.name or ""
    working_directory = {"working_directory": "./calculator"}
    # Shallow copy arguments and handle None
    if function_call.args:
        arguments = dict(function_call.args) 
    else:
        arguments = {}

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    function_result = function_map[function_name](**working_directory, **arguments)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
    )

    



    # if function_call.name == 'get_files_info':
    #     results = get_files_info(**working_directory)
    # elif function_call.name == "get_file_content":
    #     results = get_file_content(**working_directory, **arguments)
    # elif function_call.name == 'write_file':
    #     results = write_file(**working_directory, **arguments)
    # elif function_call.name == 'run_python_file':
    #     results = run_python_file(**working_directory, **arguments)

    # print(results)
    

