import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client with the API key
openai.api_key = openai_api_key

class OpenAIResponse:
    def __init__(self, response):
        self.generated_text = None
        self.total_tokens = None
        self._parse_response(response)
    
    def _parse_response(self, response):
        self.generated_text = response.choices[0].message.content.strip()
        self.total_tokens = response.usage.total_tokens
    
    def __str__(self):
        return f"Generated Text: {self.generated_text}\nTotal Tokens Used: {self.total_tokens}"

class OpenAIChatWrapper:
    def __init__(self, model="gpt-3.5-turbo", temperature=0.7, max_tokens=150, top_p=1.0):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p

    def send_message(self, messages):
        response = openai.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p
        )
        return OpenAIResponse(response)

# Example of using the OpenAIChatWrapper class
if __name__ == "__main__":
    chat_wrapper = OpenAIChatWrapper()
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain the importance of sustainable development."}
    ]
    parsed_response = chat_wrapper.send_message(messages)

    # Print the results
    print(parsed_response.generated_text)
    print(f"Total tokens used: {parsed_response.total_tokens}")

