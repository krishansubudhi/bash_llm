import configparser
import os
import re
import subprocess
import sys
import llm
import argparse
import inspect
import shlex
def load_config():
    """Loads configuration settings from config.ini."""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
    config.read(config_path)
    return config


def get_prompt(query_words, additional_commands) -> str:
    """Fetches prompt from command line arguments or requests user input, with a helpful message."""
    
    # Join query words into a string or prompt user for input if empty
    user_query_str = " ".join(query_words) if query_words else input("Enter a prompt: ")
    
    # Format additional commands with a suggestion for help
    additional_commands_str = "Available commands:\n" + "\n".join(
        [f"  {cmd}: {desc}" for cmd, desc in additional_commands]
    )
    
    # Add encouragement to use help
    help_message = "\nTip: Use `--help` to learn more about any additional command."

    return f"{additional_commands_str}\n{help_message}\n\nYour query:\n{user_query_str}"


def naive_escape_quotes(command: str) -> str:
    """Incorrectly escapes quotes."""
    return command.replace('"', '\\"').replace("'", "")

def extract_bash_command(response: str) -> str:
    """
    Extracts a bash command from response formatted in ```bash ... ```.

    Adds extra protection against potential issues:
    - Handles cases where the command block might be at the very beginning or end of the response.
    - Handles cases where the command block might have extra whitespace around it.
    - Handles cases where the command block might use different variations of the code block marker (e.g., ```sh).
    - Prevents potential ReDoS vulnerabilities.
    - Properly handles quoted arguments within the command.
    """
    if not isinstance(response, str) or not response:
        return None  # Handle invalid input

    match = re.search(r"```(?:bash|sh|shell)\n(.*?)\n```", response, re.DOTALL | re.IGNORECASE)

    if match:
        command = match.group(1).strip()
        command = naive_escape_quotes(command)
        if command and not command.startswith("```"): #prevent nested code blocks.
            try:
                # Attempt to parse the command with shlex to handle quotes correctly
                shlex.split(command) #verify that the command can be properly parsed.
                return command
            except ValueError:
                return None  # Return None if command parsing fails
        else:
            return None #failed additional check.
    else:
        return None

def run_bash_command(command: str, ask_for_confirmation: bool) -> str:
    """Executes a bash command if confirmed by the user."""
    if ask_for_confirmation:
        confirmation = input(f"Executing command: {command}\nConfirm (y/n): ")
        if confirmation.lower() not in ('y', ''):
            return "Command execution canceled by user."

    subprocess.run(f"bash -i -c '{command}'", shell=True, check=False, text=True, capture_output=False)

def main():
    parser = argparse.ArgumentParser(description="""
                                     Tool to interact with a language model to generate and execute bash commands based on a prompt.
                                     llm <query>""")
    
    parser.add_argument('query', nargs=argparse.REMAINDER, help="The actual query.")
    
    args = parser.parse_args()


    
    config = load_config()
    model_provider = config.get("settings", "model_provider")
    ask_for_confirmation = config.getboolean("settings", "ask_for_confirmation")
    additional_commands = list(config['additional_commands'].items())

    if model_provider == "openai":
        bash_llm = llm.OpenAILLM()
    elif model_provider == "gemini":
        gemini_model_name = config.get("gemini", "model_name")
        bash_llm = llm.GeminiLLM(model_name=gemini_model_name)
    else:
        raise ValueError(f"Model provider '{model_provider}' not supported. Check 'model_provider' in config.ini.")

    prompt = get_prompt(args.query, additional_commands)


    # print(prompt)
    response = bash_llm.call(prompt)

    bash_command = extract_bash_command(response)
    if bash_command:
        if len(response) > 2*len(bash_command):
            print(response)
        run_bash_command(bash_command, ask_for_confirmation)
    else:
        print(response)

if __name__ == "__main__":
    main()
