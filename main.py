import os
import sys
import argparse
from functions.get_files_info import available_functions as f1
from functions.get_file_content import available2_functions as f2
from functions.run_python_file import available3_functions as f3
from functions.write_file import available4_functions as f4
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
import json
from call_function import call_function

available_functions = f1 + f2 + f3 + f4


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt",type=str,help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()



    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("please check again your api key file")

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    
    )

    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": args.user_prompt},
        ]
    
    for i in range(20):
        

        response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
        
        )

        message = response.choices[0].message
        messages.append(message)

        if response.usage is None:
            raise RuntimeError("failed api request please check your key again")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call,args.verbose)
                messages.append(result_message)
                if not result_message.get("content"):
                    
                    raise Exception("Empty or missing content in tool result")
                        
                if args.verbose:
                    print(f"-> {result_message['content']}")
                    
            
        else:
            print(response.choices[0].message.content)
            return 
            
    print("run out of attempts (20 attempts reached)")
    sys.exit(1)    


if __name__ == "__main__":
    main()
