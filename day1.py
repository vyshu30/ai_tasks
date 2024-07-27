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

# Example of making a request to the OpenAI API
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain the importance of sustainable development."}
    ],
    temperature=0.7,
    max_tokens=150,
    top_p=1.0
)

# Parse the response using the OpenAIResponse class
parsed_response = OpenAIResponse(response)

# Print the results
print(parsed_response.generated_text)
print(f"Total tokens used: {parsed_response.total_tokens}")
