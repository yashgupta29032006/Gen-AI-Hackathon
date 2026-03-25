import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from app.core.llm import llm

class BaseAgent(ABC):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    @abstractmethod
    async def execute(self, task_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the agent's logic."""
        pass

    async def get_structured_response(self, prompt: str, system_instruction: str) -> Dict[str, Any]:
        """Helper to get JSON response from LLM."""
        full_system_instruction = (
            f"{system_instruction}\n\n"
            "CRITICAL: Your response must be a valid JSON object only. "
            "Do not include any prose, markdown formatting (no ```json), or explanations outside the JSON."
        )
        
        raw_response = await llm.generate_response(prompt, system_instruction=full_system_instruction)
        
        # Basic cleanup of markdown junk if present
        clean_response = raw_response.strip()
        if clean_response.startswith("```json"):
            clean_response = clean_response[7:-3].strip()
        elif clean_response.startswith("```"):
            clean_response = clean_response[3:-3].strip()

        try:
            return json.loads(clean_response)
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse structured response",
                "raw_content": raw_response
            }
