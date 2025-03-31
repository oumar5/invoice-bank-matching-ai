import base64
import json
from datetime import datetime
from typing import Dict, Any
from services.api.mistral_client import MistralClient
from services.utils.logging_config import setup_logger

logger = setup_logger('InvoiceAnalyzer')

class InvoiceAnalyzer:
    def __init__(self, mistral_client: MistralClient = None):
        self.mistral_client = mistral_client or MistralClient()

    def _encode_image(self, image_content: bytes) -> str:
        """
        Encode l'image en base64 pour l'envoi à Mistral
        """
        logger.debug("Encodage de l'image en base64")
        return base64.b64encode(image_content).decode('utf-8')

    def analyze(self, image_content: bytes) -> Dict[str, Any]:
        """
        Analyse une facture et extrait les informations structurées
        """
        logger.info("Début de l'analyse de la facture")
        image_base64 = self._encode_image(image_content)
        logger.debug("Image encodée en base64")

        prompt = """Analyse cette facture et extrait les informations suivantes au format JSON :
        - date : la date de la facture (format YYYY-MM-DD)
        - amount : le montant total TTC (nombre décimal)
        - vendor_name : le nom du vendeur/société
        - invoice_number : le numéro de facture
        - raw_text : le texte brut extrait

        Retourne uniquement le JSON, sans autre texte."""

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
            }
        ]

        try:
            logger.info("Envoi de la requête d'analyse à Mistral")
            content = self.mistral_client.send_message(messages)
            
            # Nettoyer la réponse pour s'assurer qu'elle est en JSON valide
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            result = json.loads(content)
            logger.info("Analyse de la facture réussie")
            logger.info(f"Résultat de l'analyse: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # Convertir la date si elle existe
            if result.get('date'):
                try:
                    result['date'] = datetime.strptime(result['date'], '%Y-%m-%d')
                    logger.debug(f"Date convertie: {result['date']}")
                except Exception as e:
                    logger.warning(f"Erreur lors de la conversion de la date: {str(e)}")
                    result['date'] = None
            
            # Convertir le montant en float
            if result.get('amount'):
                try:
                    result['amount'] = float(str(result['amount']).replace(',', '.'))
                    logger.debug(f"Montant converti: {result['amount']}")
                except Exception as e:
                    logger.warning(f"Erreur lors de la conversion du montant: {str(e)}")
                    result['amount'] = None

            return result

        except Exception as e:
            logger.error(f"Erreur lors de l'analyse de la facture: {str(e)}")
            return {
                'date': None,
                'amount': None,
                'vendor_name': None,
                'invoice_number': None,
                'raw_text': str(e),
                'error': str(e)
            } 