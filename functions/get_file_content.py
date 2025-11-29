import os
from functions.config import MAX_CHAR
from google.genai import types

def get_file_content(working_directory, file_path):
    
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_file = os.path.abspath(os.path.join(working_directory, file_path))

        # Debugging
        # print(abs_working_dir)
        # print(abs_target_file)
        
        # check if outside working directory
        if os.path.commonpath([abs_working_dir, abs_target_file]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory\n'
        
        # check if the file is valid
        if not os.path.isfile(abs_target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"\n'

        with open(abs_target_file, "r") as f:
            # Truncate the string if it's too long
            file_content = f.read(MAX_CHAR)
        
            if len(f.read()) > MAX_CHAR:
                file_content = file_content + f'\n\n[...File "{file_path}" truncated at 10000 characters]'
            
        return file_content
            
    except Exception as e:
        return f'Error: {e}'
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content of a file in the specified file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=['file_path'],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the file that will be read from in the working directory.",
            ),
        },
    ),
)