import os
import sys
from dotenv import load_dotenv
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

# Generate content using Gemini model
response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages
)

# Keeps track of use of '--verbose' tag.
verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"

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
