import os
from google.genai import types

def write_file(working_directory, file_path, content):
    
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_file = os.path.abspath(os.path.join(working_directory, file_path))
        target_file_dirname = os.path.dirname(abs_target_file)

        # check if outside working directory
        if os.path.commonpath([abs_working_dir, abs_target_file]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        # create the directory if it does not exist
        if not os.path.exists(target_file_dirname):
            os.makedirs(target_file_dirname)

        with open(abs_target_file, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file within a working directory.  If the file doesn't exist, then it will create it.  If the file has content, then it will be overwritten.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=['file_path', 'content'],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the file that will be written to.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text that will be written to a file.",
            ),
        },
    ),
)