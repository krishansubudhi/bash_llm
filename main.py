import openai
from dotenv import load_dotenv
import os
import sys

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def call_llm(prompt):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {   "role": "system", "content": \
             "You are an assistant running on bash. User is asking questions from their shell. Keep the response concise and helpful."\
             f"current_directory = {os.getcwd()}"},
            {   "role": "user", "content": prompt}
        ]
    )
    print(response.choices[0].message.content)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("enter a prompt")
        prompt = input()
    prompt = " ".join(sys.argv[1:])
    call_llm(prompt)