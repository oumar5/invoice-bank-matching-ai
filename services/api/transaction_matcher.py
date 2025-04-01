import json
import pandas as pd
from typing import Dict, Any, List
from services.api.mistral_client import MistralClient
from services.utils.logging_config import setup_logger
from datetime import datetime, timedelta
import os

logger = setup_logger('TransactionMatcher')

class TransactionMatcher:
    def __init__(self, mistral_client: MistralClient = None):
        self.mistral_client = mistral_client or MistralClient()
        self.prompts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'prompts')

    def _load_prompt(self, prompt_file: str) -> str:
        """
        Charge un prompt depuis un fichier
        """
        prompt_path = os.path.join(self.prompts_dir, prompt_file)
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            logger.error(f"Erreur lors du chargement du prompt {prompt_file}: {str(e)}")
            return ""

    def _parse_date(self, date_str: str) -> datetime:
        """
        Parse une date string dans différents formats
        """
        formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%d/%m/%Y',
            '%m/%d/%Y',
            '%Y-%m-%d %H:%M:%S',
            '%Y/%m/%d %H:%M:%S'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
                
        raise ValueError(f"Format de date non supporté: {date_str}")

    def _format_transaction(self, row: pd.Series) -> str:
        """
        Formate une transaction en texte en utilisant les colonnes spécifiques du CSV
        """
        logger.debug(f"Formatage de la transaction: {row.to_dict()}")
        parts = []
        
        # Date
        if 'date' in row:
            parts.append(f"Date: {row['date']}")
            
        # Montant et devise
        if 'amount' in row and 'currency' in row:
            parts.append(f"Montant: {row['amount']} {row['currency']}")
        elif 'amount' in row:
            parts.append(f"Montant: {row['amount']}")
            
        # Vendeur
        if 'vendor' in row:
            parts.append(f"Vendeur: {row['vendor']}")
            
        formatted = ", ".join(parts)
        logger.debug(f"Transaction formatée: {formatted}")
        return formatted

    def extract_invoice_info(self, invoice_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrait les informations clés de la facture en utilisant le LLM
        """
        logger.info("Début de l'extraction des informations de la facture")
        
        # Préparer les données de la facture avec gestion des valeurs None
        vendor_name = invoice_data.get('vendor_name', '')
        raw_text = invoice_data.get('raw_text', '')
        
        invoice_text = f"""Facture :
        - Date: {invoice_data.get('date', '')}
        - Montant: {invoice_data.get('amount', '')}
        - Vendeur: {vendor_name.replace("'", "\\'") if vendor_name else ''}
        - Numéro: {invoice_data.get('invoice_number', '')}
        - Texte brut: {raw_text.replace("'", "\\'") if raw_text else ''}
        """

        # Charger le prompt depuis le fichier
        prompt_template = self._load_prompt('invoice_extraction.txt')
        if not prompt_template:
            logger.error("Impossible de charger le prompt d'extraction")
            return None

        # Remplacer le placeholder dans le prompt
        prompt = prompt_template.format(invoice_text=invoice_text)

        messages = [
            {"role": "user", "content": prompt}
        ]

        try:
            logger.info("Envoi de la requête d'extraction à Mistral")
            content = self.mistral_client.send_message(messages)
            
            # Nettoyer la réponse pour s'assurer qu'elle est en JSON valide
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            result = json.loads(content)
            logger.info("Extraction terminée avec succès")
            logger.info(f"Résultat de l'extraction: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction: {str(e)}")
            return None

    def find_matching_transaction(self, invoice_info: Dict[str, Any], transactions_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Trouve la transaction correspondante en utilisant les critères stricts
        """
        if not invoice_info:
            return {
                'match_found': False,
                'confidence_score': 0.0,
                'transaction_date': None,
                'transaction_amount': None,
                'transaction_vendor': None,
                'matching_reason': "Impossible d'extraire les informations de la facture"
            }

        # Convertir la date de la facture en datetime
        try:
            invoice_date = self._parse_date(invoice_info['date'])
        except ValueError as e:
            return {
                'match_found': False,
                'confidence_score': 0.0,
                'transaction_date': None,
                'transaction_amount': None,
                'transaction_vendor': None,
                'matching_reason': f"Format de date invalide: {str(e)}"
            }

        # Filtrer les transactions par date (7 jours avant/après)
        date_range = transactions_df['date'].apply(
            lambda x: invoice_date - timedelta(days=7) <= self._parse_date(x) <= invoice_date + timedelta(days=7)
        )
        date_filtered_df = transactions_df[date_range]

        # Filtrer par montant exact
        amount_filtered_df = date_filtered_df[
            date_filtered_df['amount'].astype(float) == float(invoice_info['amount'])
        ]

        # Filtrer par vendeur exact
        vendor_filtered_df = amount_filtered_df[
            amount_filtered_df['vendor'].str.lower() == invoice_info['vendor_name'].lower()
        ]

        if not vendor_filtered_df.empty:
            # Trouver la transaction la plus proche en date
            best_match = vendor_filtered_df.iloc[0]
            return {
                'match_found': True,
                'confidence_score': 1.0,
                'transaction_date': best_match['date'],
                'transaction_amount': best_match['amount'],
                'transaction_vendor': best_match['vendor'],
                'matching_reason': "Correspondance exacte trouvée (date, montant et vendeur)"
            }
        else:
            return {
                'match_found': False,
                'confidence_score': 0.0,
                'transaction_date': None,
                'transaction_amount': None,
                'transaction_vendor': None,
                'matching_reason': "Aucune transaction ne correspond aux critères stricts"
            }

    def match_invoice_with_transactions(self, invoice_data: Dict[str, Any], transactions_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Trouve la meilleure correspondance entre une facture et les transactions
        """
        # Étape 1 : Extraire les informations de la facture
        invoice_info = self.extract_invoice_info(invoice_data)
        
        # Étape 2 : Trouver la transaction correspondante
        return self.find_matching_transaction(invoice_info, transactions_df) 