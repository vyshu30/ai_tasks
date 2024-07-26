import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')


# Example of making a request to the OpenAI API

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain the importance of sustainable development."}
    ],
    max_tokens=150
)
print(response)
#  print(response.choices[0].message['content'].strip())
# Python dictionary (simulated API response)
response_dict = {
    "id": "cmpl-5uIvfBq6I47zr1nTQjVZ9g5F",
    "object": "text_completion",
    "created": 1623312226,
    "model": "text-davinci-003",
    "choices": [
        {
            "text": "Your generated text here.",
            "index": 0,
            "logprobs": None,
            "finish_reason": "length"
        }
    ],
    "usage": {
        "prompt_tokens": 5,
        "completion_tokens": 10,
        "total_tokens": 15
    }
}

# Extract and print total_tokens
total_tokens = response_dict['usage']['total_tokens']
print(total_tokens)
