import sys
import llm
import configparser
import os

def get_prompt() -> str:
    """Fetches prompt from command line arguments or asks for input."""
    return " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter a prompt: ")



if __name__ == "__main__":
    config = configparser.ConfigParser()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "config.ini")
    config.read(config_path)
    model_provider = config.get("settings", "model_provider")
    
    if model_provider == "openai":
        bash_llm = llm.OpenAILLM()
    elif model_provider == "gemini":
       bash_llm = llm.GeminiLLM()
    else:
        raise AttributeError(f"Model provider {model_provider} not supported. Add correct 'model_provider' in config.ini")

    prompt = get_prompt()
    bash_llm.call(prompt)
