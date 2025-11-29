import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
# Not intended for use in production environment
    
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_file = os.path.abspath(os.path.join(working_directory, file_path))

        # Debug
        # print(f'abs_working_dir: {abs_working_dir}')
        # print(f'abs_target_file: {abs_target_file}')
        # print(f'filetype 2: {file_path[-3:]}')

        # check if outside working directory
        if os.path.commonpath([abs_working_dir, abs_target_file]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # check if the file exists
        if not os.path.exists(abs_target_file):
            return f'Error: File "{file_path}" not found.'
        
        if file_path[-3:] != '.py':
            return f'Error: "{file_path}" is not a Python file.'
        
        commands = []
        commands.append("python")
        commands.append(f'{abs_target_file}')

        if args:
            commands.extend(args)
  
        proc = subprocess.run(
            commands, 
            cwd = abs_working_dir, 
            timeout=30,         # maximum 30 second runtime
            capture_output=True,
            text = True         # otherwise it would return bytes
        )

        # build a list of strings and then combine them into a single output string
        stderr = proc.stderr
        stdout = proc.stdout
        result = []

        if stderr:
            result.append(f'STDERR: {stderr}')

        if stdout:
            result.append(f'STDOUT: {stdout}')

        if not stdout and not stderr and proc.returncode == 0:
            result.append("No output produced.")

        if proc.returncode != 0:
            result.append(f'Process exited with code {proc.returncode}')

        return "\n ".join(result)

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python program within a working directory. It returns a single string with stdout and stderr values when successful and return codes when not successful.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=['file_path'],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The name of the file that will be run from in the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="A list of optional arguments that can be passed to Python",
            ),
        },
    ),
)