import os

def write_file(working_directory, file_path, content):

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not (abs_file_path == abs_working_dir or abs_file_path.startswith(abs_working_dir + os.sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    dir_to_create = os.path.dirname(file_path)
    if dir_to_create:
        if not os.path.exists(dir_to_create):
            os.makedirs(dir_to_create)

    try:
        with open(file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"
        
