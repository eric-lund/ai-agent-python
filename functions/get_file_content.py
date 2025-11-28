import os
from functions.config import MAX_CHAR

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