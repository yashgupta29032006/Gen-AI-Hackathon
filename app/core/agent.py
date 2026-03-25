import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from app.core.llm import llm

import re

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
            "Do not include any prose or explanations."
        )
        
        raw_response = await llm.generate_response(prompt, system_instruction=full_system_instruction)
        
        # Robust JSON extraction using regex
        json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
        if json_match:
            clean_response = json_match.group(0)
        else:
            clean_response = raw_response.strip()

        try:
            return json.loads(clean_response)
        except json.JSONDecodeError:
            return {
                "error": "Failed to parse structured response",
                "raw_content": raw_response
            }
