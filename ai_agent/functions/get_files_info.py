import os
from google.genai import types

def get_files_info(working_directory, directory=None):

    if directory is None:
        directory = "."

    # Create full path
    full_path = os.path.abspath(os.path.join(working_directory, directory))

    # Checking whether directory exists
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    # Ensure full_path is inside working_directory
    abs_working_dir = os.path.abspath(working_directory)
    if not (full_path == abs_working_dir or full_path.startswith(abs_working_dir + os.sep)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    try:
        # Get the list of files/directories
        entries = os.listdir(full_path)

        # Build detailed info lines
        entry_info = []
        for entry in entries:
            entry_path = os.path.join(full_path, entry)
            file_size = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)
            entry_info.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(entry_info)

    except Exception as e:
        return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a single file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The location of the file.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional command-line arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The full path to the Python file to run.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command-line arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file to the working directory or a subdirectory, with the provided content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path (from the working directory) where the file will be written.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text or data to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)