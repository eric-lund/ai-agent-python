import os 
from dotenv import load_dotenv
from google import genai

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        print("the key variable is empty")

    client = genai.Client(api_key=api_key)

    model ="gemini-2.0-flash-001"
    contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    print("Hello from ai-agent-python!")

    clientModel = client.models.generate_content(model=model, contents=contents)
    print(clientModel.text)
    print(f"Prompt tokens: {clientModel.usage_metadata.prompt_token_count}\nResponse tokens: {clientModel.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
