import argparse
import sys
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from  prompts import system_prompt


def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv
    args = []

    for arg in sys.argv[1:]:
         if not arg.startswith("--"):
              args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    
    user_prompt = " ".join(args)

    if verbose:
         print(f"User prompt: {user_prompt}\n")

    
    messages = [
        types.Content(role= "user", parts=[types.Part(text=user_prompt)]),

    ]
   

    generate_content(client, messages, verbose)
    

def generate_content(client, messages, verbose):
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents= messages,
            config= types.GenerateContentConfig(system_instruction=system_prompt),
        )

        if verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        print(response.text)



if __name__ == "__main__":
    main()
