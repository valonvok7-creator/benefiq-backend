from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class EmbeddingService:
    def __init__(self):
        api_key = os.getenv("INFOMANIAK_API_KEY")
        base_url = os.getenv("INFOMANIAK_BASE_URL")

        if not api_key or not base_url:
            raise ValueError("Clé API ou URL manquante (INFOMANIAK_API_KEY ou INFOMANIAK_BASE_URL)")

        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def embed(self, text: str):
        response = self.client.embeddings.create(
            model="mini_lm_l12_v2",
            input=text
        )
        return response.data[0].embedding

