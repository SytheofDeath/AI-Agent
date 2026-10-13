import os
import argparse
import sys
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_functions import available_functions
from call_functions import call_function
import json

def main():
    parser = argparse.ArgumentParser(description="Bootdev-AI-Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("OPENROUTER_API_KEY not set")

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
            tools=available_functions,
        )
        if not response.usage:
            raise RuntimeError("API response appears to be malformed")

        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls == None:
            print(response.choices[0].message.content)
            break
        else:
            for tool_call in message.tool_calls:
                #function_args = json.loads(tool_call.function.arguments or "{}")
                #print(f"Calling function: {tool_call.function.name}({function_args})")
                result = call_function(tool_call, args.verbose)
                if result['content'] == "":
                    raise Exception("Result empty")
                if args.verbose == True:
                    print(f"-> {result['content']}")
                messages.append(result)
    else:
        print("Agent has hit iteration limit")
        sys.exit(1)

if __name__ == "__main__":
    main()
