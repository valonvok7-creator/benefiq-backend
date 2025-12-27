import os
import requests
from typing import List, Dict, Any, Optional


class LLMService:
    def __init__(self) -> None:
        # Endpoint AlpineAI (compatible OpenAI)
        self.api_url = "https://api.alpine.ai/v1/chat/completions"

        # Clé API depuis le .env
        self.api_key = os.getenv("ALPINEAI_API_KEY", "")

        if not self.api_key:
            raise ValueError("ALPINEAI_API_KEY manquante dans l'environnement (.env)")

        # Modèle par défaut AlpineAI
        self.default_model = "meta-llama-3-8b-instruct"

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def _payload(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        return payload

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Appel simple : prompt utilisateur + option system prompt.
        """
        messages: List[Dict[str, str]] = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        return self._call(messages, model, temperature, max_tokens)

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Appel avancé : liste de messages (system/user/assistant).
        """
        return self._call(messages, model, temperature, max_tokens)

    def _call(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str],
        temperature: float,
        max_tokens: Optional[int],
    ) -> str:
        try:
            payload = self._payload(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            response = requests.post(
                self.api_url,
                json=payload,
                headers=self._headers(),
                timeout=60,
            )
            response.raise_for_status()

            data = response.json()
            return data["choices"][0]["message"]["content"]

        except Exception as e:
            return f"Erreur LLM (AlpineAI) : {str(e)}"
