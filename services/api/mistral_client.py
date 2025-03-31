import json
import requests
import time
from typing import Dict, Any, List
from config.settings import (
    MISTRAL_API_KEY,
    MISTRAL_API_BASE_URL,
    MISTRAL_MODEL,
    MAX_RETRIES,
    REQUEST_TIMEOUT,
    MAX_TOKENS,
    TEMPERATURE
)
from services.utils.logging_config import setup_logger

logger = setup_logger('MistralClient')

class MistralClient:
    def __init__(self, api_key: str = MISTRAL_API_KEY):
        self.api_key = api_key
        self.base_url = MISTRAL_API_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _make_request_with_retry(self, messages: List[Dict[str, Any]], max_retries: int = MAX_RETRIES) -> Any:
        """
        Fait une requête à l'API avec retry en cas d'erreur
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"Tentative {attempt + 1}/{max_retries} d'appel à l'API Mistral")
                logger.info(f"Messages envoyés: {json.dumps(messages, indent=2, ensure_ascii=False)}")
                
                payload = {
                    "model": MISTRAL_MODEL,
                    "messages": messages,
                    "temperature": TEMPERATURE,
                    "max_tokens": MAX_TOKENS
                }
                
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json=payload,
                    timeout=REQUEST_TIMEOUT
                )
                
                if response.status_code != 200:
                    logger.error(f"Erreur API: {response.status_code} - {response.text}")
                    raise Exception(f"Status: {response.status_code}. Message: {response.text}")
                
                result = response.json()
                logger.info("Réponse reçue de l'API Mistral")
                logger.info(f"Réponse: {json.dumps(result, indent=2, ensure_ascii=False)}")
                
                if not result.get('choices') or not result['choices'][0].get('message', {}).get('content'):
                    raise Exception("Réponse invalide de l'API")
                    
                return result
                
            except Exception as e:
                logger.error(f"Erreur lors de l'appel à l'API (tentative {attempt + 1}): {str(e)}")
                if attempt == max_retries - 1:
                    logger.error("Nombre maximum de tentatives atteint")
                    raise e
                wait_time = 2 ** attempt
                logger.info(f"Attente de {wait_time} secondes avant la prochaine tentative")
                time.sleep(wait_time)

    def send_message(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Envoie un message à l'API et retourne la réponse
        """
        response = self._make_request_with_retry(messages)
        return response['choices'][0]['message']['content'] 