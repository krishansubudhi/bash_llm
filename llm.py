import os
import openai
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class BaseLLM:
    """Base class for setting up and calling language models."""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.system_instruction = self.get_system_instruction()

    def get_system_instruction(self) -> str:
        """Generates system instruction with the current directory."""
        return (
            f"Your name is {self.model_name}."
            "You are an assistant running on bash. User is asking questions from their shell. "
            "Keep the response concise and helpful."
            f" Current directory: {os.getcwd()}"
        )

    def call(self, prompt: str):
        """Placeholder for model-specific API calls."""
        raise NotImplementedError("This method should be overridden in subclasses")


class OpenAILLM(BaseLLM):
    """Class for OpenAI LLM integration."""

    def __init__(self, model_name: str = "gpt-4o"):
        super().__init__(model_name)
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI()

    def call(self, prompt: str):
        """Calls OpenAI's chat completion API."""
        response =  self.client.chat.completions.create(
            model="gpt-4o",
            messages =[
                        {"role": "system", "content": self.system_instruction},
                        {"role": "user", "content": prompt}
                    ]
        )

        print(response.choices[0].message.content)


class GeminiLLM(BaseLLM):
    """Class for Google Gemini LLM integration."""

    def __init__(self, model_name: str = "gemini-1.5-flash"):
        super().__init__(model_name)
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(self.model_name, system_instruction=self.system_instruction)

    def call(self, prompt: str):
        """Calls Google's Gemini API."""
        response = self.model.generate_content(prompt)
        print(response.text)
