import openai
import os
import json
import re
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatMemory:
    def __init__(self, file_path="chat_memory.json"):
        self.file_path = file_path
        self.history = self.load_history()
        self.parameters = {}  # Store user-defined parameters
    
    def add_user_message(self, message):
        self.history.append({"role": "user", "content": message})
        self.save_history()
    
    def add_assistant_message(self, message):
        self.history.append({"role": "assistant", "content": message})
        self.save_history()
    
    def get_history(self):
        return self.history
    
    def save_history(self):
        with open(self.file_path, "w") as file:
            json.dump({"history": self.history, "parameters": self.parameters}, file, indent=4)
    
    def load_history(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                data = json.load(file)
                self.parameters = data.get("parameters", {})
                return data.get("history", [{"role": "system", "content": "You are a helpful assistant."}])
        else:
            return [{"role": "system", "content": "You are a helpful assistant."}]
    
    def set_parameter(self, key, value):
        self.parameters[key] = value
    
    def get_parameter(self, key):
        return self.parameters.get(key, "I don't have information about that.")

def chat_with_openai(messages):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=150,
            top_p=1.0
        )
        # print(response)  # Debugging: Print the entire response object
        # Correctly access the response content
        content = response.choices[0].message.content
        return content
    except Exception as e:
        print(f"Error interacting with OpenAI API: {e}")
        return "I'm having trouble accessing the API right now."

def extract_parameter(message):
    # Simple regex to extract key-value pairs
    match = re.match(r"I want to store (\w+) as (.+)", message, re.IGNORECASE)
    if match:
        key, value = match.groups()
        return key, value
    return None, None

def main():
    print("Chatbot is running. Type 'exit' to end the conversation.")
    
    # Create an instance of ChatMemory to manage conversation history and parameters
    chat_memory = ChatMemory()

    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        
        # Extract and store any parameters if specified
        key, value = extract_parameter(user_input)
        if key:
            chat_memory.set_parameter(key, value)
            response = f"Got it! I’ll remember that {key} is {value}."
        else:
            # Add user input to the conversation history
            chat_memory.add_user_message(user_input)

            # Get response from the assistant based on the entire conversation history
            response = chat_with_openai(chat_memory.get_history())

            # Add the assistant's response to the conversation history
            chat_memory.add_assistant_message(response)
        
        # Print the assistant's response
        print(f"Assistant: {response}")

if __name__ == "__main__":
    main()
