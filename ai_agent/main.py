import os
import sys
from dotenv import load_dotenv
from functions.get_files_info import available_functions, schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file, get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Check if API key is loaded
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment.")
    sys.exit(1)

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Check if prompt is provided
if len(sys.argv) < 2:
    print("Error: No prompt provided.")
    sys.exit(1)

user_prompt = sys.argv[1]

# A list that keeps track of past messages
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Generate content using Gemini model
response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages,
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
    )
)

# Check for verbose flag earlier
verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"

def call_function(function_call_part, verbose=False):
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"

    function_name = function_call_part.name
    function_to_call = function_map.get(function_call_part.name)
   
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_to_call:
        result = function_to_call(**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )


if response.function_calls and len(response.function_calls) > 0:
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose=verbose)
        # Check for required function response or raise fatal error
        parts = function_call_result.parts
        if not parts or not hasattr(parts[0], "function_response") or parts[0].function_response is None:
            raise Exception("No function response in Content object")
        # Always print function result so CLI can test stdout!
print(parts[0].function_response.response)
if verbose:
    print(f"-> {parts[0].function_response.response}")

else:
    # Print model response and token usage
    if verbose:
        print(f'User prompt: {user_prompt}"')  
        print(f"Prompt tokens:", response.usage_metadata.prompt_token_count)
        print(f"Response tokens:", response.usage_metadata.candidates_token_count)

    print(response.text)


def main():
    print("Hello from ai-agent!")


if __name__ == "__main__":
    main()
