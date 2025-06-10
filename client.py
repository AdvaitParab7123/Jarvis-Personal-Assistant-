# client.py
import google.generativeai as genai

class PersonalAIAgent:
    def __init__(self, api_key: str):
        # Configure the Google Gemini API key directly
        genai.configure(api_key="AIzaSyAE3qIXXkEoLdugrDzgtStC6iWQChvBWL4")

        # Initialize the model. 'gemini-1.5-flash' is a good balance.
        self.model = genai.GenerativeModel('gemini-1.5-flash')

        # Start a chat session. Gemini's `start_chat` manages the history internally.
        # We'll set the "system" instruction by priming the chat history.
        self.chat = self.model.start_chat(history=[
            # This is how you set the "system" role in Gemini by priming the conversation
            {"role": "user", "parts": ["You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"]},
            {"role": "model", "parts": ["Understood. I am Jarvis, ready to assist you."]}
        ])

    def get_response(self, user_message: str) -> str:
        try:
            response = self.chat.send_message(user_message)
            return response.text
        except Exception as e:
            # Print the error for debugging, but provide a friendly fallback
            print(f"Error communicating with Gemini: {e}")
            return "I am sorry, I am unable to process that request right now."