import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not (abs_file_path == abs_working_dir or abs_file_path.startswith(abs_working_dir + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found'

    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    command_to_run = ['python', abs_file_path] + args
    
    try:
        output_message = []

        completed_process = subprocess.run(
            command_to_run, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            cwd=abs_working_dir,
            timeout=30, 
            text=True
        )

        if completed_process.stdout:
            output_message.append(f"STDOUT: {completed_process.stdout}")
            
        if completed_process.stderr:
            output_message.append(f"STDERR: {completed_process.stderr}")

        if completed_process.returncode != 0:
            output_message.append(f"Process exited with code {completed_process.returncode}")
    
        final_result = "".join(output_message)

        if not final_result:
            return "No output produced"
        else:
            return final_result

    except Exception as e:
        return f"Error: executing Python file: {e}"
