import os 
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():

    if len(sys.argv) - 1 == 0:
        print("Prompt is missing.  Exiting program.")
        sys.exit(1)

    # convert sys.argv list to a single string, excluding the app name
    user_prompt = " ".join(sys.argv[1:])
    
    # capture command argument if one was passed; assumes 3rd position
    if (any("--" in x for x in sys.argv[1:])):
        command_prompt = sys.argv[2]
    else:
        command_prompt = ''
    
    welcome_message = "Hello from ai-agent-python!"

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        print("the key variable is empty")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    if (command_prompt == "--verbose"):
        print(welcome_message)
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
        print(response.text)
    else:
        print(welcome_message)
        print(response.text)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
