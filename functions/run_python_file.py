import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try: 
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        

        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not abs_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
    
   
        command = ["python", abs_file_path]
        output = []
        if args:
            command.extend(args)
        
        complete_process = subprocess.run(command,cwd=working_directory,capture_output=True,text=True,timeout=30.0 )

        if complete_process.returncode != 0:
            output.append(f"Process exited with code {complete_process.returncode}")
        if not complete_process.stdout and not complete_process.stderr:
            output.append("No output produced")

       

        if complete_process.stdout:
            output.append(f"STDOUT: {complete_process.stdout}")

        if complete_process.stderr:
            output.append(f"STDERR: {complete_process.stderr}")

    
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file within the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of arguments to pass to the Python script",
            ),
        },
        required=["file_path"],
    ),
)
