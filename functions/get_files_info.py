import os

def get_files_info(working_directory, directory="."):
    
    try:
        abs_working_dir = os.path.normcase(os.path.abspath(working_directory))
        abs_target_dir = os.path.abspath(os.path.join(working_directory, directory))

        # Debugging
        # print(f'abs_working_dir: {abs_working_dir}')
        # print(f'abs_target_dir: {abs_target_dir}')
        # print(f'commonpath: {os.path.commonpath([abs_working_dir, abs_target_dir]) == abs_working_dir}')

        # check if it is a valid directory
        if not os.path.isdir(abs_target_dir):
            return f'Error: "{directory}" is not a directory'

        # check if outside working directory
        if os.path.commonpath([abs_working_dir, abs_target_dir]) != abs_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            
        contents = os.listdir(abs_target_dir)
        lines = []

        # create a list of the filename and metadata
        for content in contents:
            full_path = os.path.join(abs_target_dir, content)
            lines.append(f'- {content}:  file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}')
            
        return '\n'.join(lines)
        
    # return errors raised by standard library functions
    except Exception as e:
        return f'Error: {e}'