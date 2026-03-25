import os
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class GeminiLLM:
    def __init__(self, model_name: str = None):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables.")
        
        genai.configure(api_key=api_key)
        self.model_name = model_name or os.getenv("GOOGLE_API_MODEL", "gemini-2.0-flash")
        self.model = genai.GenerativeModel(self.model_name)

    async def generate_response(self, prompt: str, system_instruction: str = None) -> str:
        try:
            if system_instruction:
                # Use system_instruction if supported by the model version or prepend to prompt
                chat = self.model.start_chat(history=[])
                full_prompt = f"System Instruction: {system_instruction}\n\nUser: {prompt}"
                response = chat.send_message(full_prompt)
            else:
                response = self.model.generate_content(prompt)
            
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"

llm = GeminiLLM()
