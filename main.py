import sys
import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def generate_content(client, messages, model_name="gemini-2.5-flash"):
    result = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt,
                                               temperature=0,
                                               tools=[available_functions]
                                               ),
            )
    return result


def is_valid_content(content):
    """
    Returns True if the Content object has at least one part with valid data.
    Returns False if all parts are empty/None.
    """
    if not content or not content.parts:
        return False

    # Part(video_metadata=None
    # thought=None
    # code_execution_result=None
    # executable_code=None
    # file_data=None
    # function_call=None
    # function_response=None
    # inline_data=None
    # text=None)
    for part in content.parts:
        # Check if any required field is set (not None)
        if (part.text is not None or 
            part.function_call is not None or 
            part.function_response is not None or 
            part.inline_data is not None or 
            part.file_data is not None or 
            part.executable_code is not None or 
            part.code_execution_result is not None or
            part.video_metadata is not None or
            part.thought is not None):
            
            # Optional: Catch empty strings which can also cause 400 errors
            if part.text is not None and not part.text.strip():
                continue 
                
            return True

    return False





def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    for _ in range(20):
        # call the model, handle responses, etc.
        result = generate_content(client, messages)
        if result.candidates:
            for c in result.candidates:
                if is_valid_content(c.content):
                    messages.append(c.content)

        if result.function_calls:
            function_results = []
            for function_call in result.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args}")
                function_call_result =  call_function(function_call)
                if not function_call_result.parts:
                      raise RuntimeError(f'function_call "{function_call.name}" has empty parts in result')
                if not isinstance(function_call_result.parts[0].function_response, types.FunctionResponse):
                      raise RuntimeError(f'expected function_call "{function_call.name}" response to have parts[0].function_response')
                if is_valid_content(function_call_result):
                    function_results.append(function_call_result)
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.extend(function_results)
        else:
            break

    if result.function_calls:
        print("Did not reach final answer in 20 iterations")
        sys.exit(1)

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {result.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {result.usage_metadata.candidates_token_count}")

    if result.text:
        print(result.text)


if __name__ == "__main__":
    main()
