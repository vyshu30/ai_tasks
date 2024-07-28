import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging

# Suppress warnings from absl library
logging.getLogger('absl').setLevel(logging.ERROR)

# Load environment variables from .env file
load_dotenv()
genai_api_key = os.getenv("GEMINI_API_KEY")
if not genai_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=genai_api_key)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "essay on AI\n",
            ],
        },
        {
            "role": "model",
            "parts": [
                "## The Dawn of a New Era: An Essay on Artificial Intelligence\n\nArtificial Intelligence (AI) has emerged from the realm of science fiction into our everyday lives, transforming industries, altering societal norms, and prompting profound ethical considerations. This essay explores the multifaceted impact of AI, examining its potential, limitations, and the critical role of responsible development and deployment. \n\nAI encompasses a range of technologies designed to mimic human cognitive abilities, including learning, problem-solving, and decision-making. Its rapid advancements have spurred innovation in diverse fields. In healthcare, AI assists in diagnosing diseases, personalizing treatments, and accelerating drug discovery. In finance, it enhances risk assessment, fraud detection, and customer service. Autonomous vehicles, powered by AI, promise to revolutionize transportation, increasing safety and efficiency. \n\nThe potential benefits of AI are undeniable, but its development raises significant ethical concerns. The use of AI in facial recognition technology raises privacy issues, while algorithmic bias can perpetuate societal inequalities. The displacement of jobs by automation requires careful consideration of retraining programs and social safety nets. Furthermore, the development of autonomous weapons systems raises profound ethical dilemmas, demanding robust international regulations. \n\nNavigating these challenges requires a multi-pronged approach. Governments must establish clear ethical guidelines and regulatory frameworks to ensure responsible AI development. Companies need to prioritize transparency and accountability, building trust with users by explaining how AI algorithms work and addressing concerns about bias. Researchers must continue to develop AI systems that are robust, fair, and aligned with human values.\n\nThe future of AI is a tapestry woven with both opportunity and uncertainty. By embracing its potential while addressing its limitations, we can harness the power of AI to create a more equitable, sustainable, and prosperous future for all. The responsibility lies with each of us, as individuals, governments, and companies, to shape the development and deployment of AI in a way that benefits humanity as a whole. \n\nThis essay merely scratches the surface of the complex and evolving landscape of AI. As technology continues to advance, the dialogue surrounding its impact must be ongoing, encompassing diverse perspectives and engaging with the ethical implications of its widespread use. The dawn of a new era is upon us, and the choices we make today will shape the world of tomorrow. \n",
            ],
        },
    ]
)

def send_message_to_chatbot(message):
    """Function to send a message to the chatbot and return the response."""
    response = chat_session.send_message(message)
    return response.text

# Example usage of the function
user_message = "Tell me about the impact of AI on healthcare."
response_text = send_message_to_chatbot(user_message)
print(response_text)
