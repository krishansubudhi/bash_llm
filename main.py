import configparser
import os
import re
import subprocess
import sys
import llm

def load_config():
    """Loads configuration settings from config.ini."""
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
    config.read(config_path)
    return config

def get_prompt() -> str:
    """Fetches prompt from command line arguments or requests user input."""
    return " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter a prompt: ")

def extract_bash_command(response: str) -> str:
    """Extracts a bash command from response formatted in ```bash ... ```."""
    match = re.search(r"```bash\n(.*?)\n```", response, re.DOTALL)
    return match.group(1).strip() if match else None

def run_bash_command(command: str, ask_for_confirmation: bool) -> str:
    """Executes a bash command if confirmed by the user."""
    if ask_for_confirmation:
        confirmation = input(f"Executing command: {command}\nConfirm (y/n): ")
        if confirmation.lower() not in ('y', ''):
            return "Command execution canceled by user."

    subprocess.run(command, shell=True, check=False, text=True, capture_output=False)

def main():
    config = load_config()
    model_provider = config.get("settings", "model_provider")
    ask_for_confirmation = config.getboolean("settings", "ask_for_confirmation")

    if model_provider == "openai":
        bash_llm = llm.OpenAILLM()
    elif model_provider == "gemini":
        bash_llm = llm.GeminiLLM()
    else:
        raise ValueError(f"Model provider '{model_provider}' not supported. Check 'model_provider' in config.ini.")

    prompt = get_prompt()
    response = bash_llm.call(prompt)

    bash_command = extract_bash_command(response)
    if bash_command:
        run_bash_command(bash_command, ask_for_confirmation)
    else:
        print(response)

if __name__ == "__main__":
    main()
