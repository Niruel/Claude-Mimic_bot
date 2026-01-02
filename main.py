import argparse
import sys
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from  prompts import system_prompt
from call_function import available_functions, call_function


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
   
    for _ in range(20):
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations ({20}) reached")
    sys.exit(1)
    

def generate_content(client, messages, verbose):
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents= messages,
            config= types.GenerateContentConfig(tools=[available_functions], 
                                                system_instruction=system_prompt),
        )
        if not response.usage_metadata:
            raise RuntimeError("Gemini API response appears to be malformed")
        
            
        if verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        if not response.function_calls:
            return response.text
        

        function_responses = []
        for function_call in  response.function_calls:
            result = call_function(function_call, verbose)

            if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
                raise RuntimeError(f"Empty function response for {function_call.name}")
            if verbose:
                print(f"-> {result.parts[0].function_response.response}")
            function_responses.append(result.parts[0])
        messages.append(types.Content(role="user", parts=function_responses))



if __name__ == "__main__":
    main()
