import json
import pandas as pd
from typing import Dict, Any, List
from services.api.mistral_client import MistralClient
from services.utils.logging_config import setup_logger

logger = setup_logger('TransactionMatcher')

class TransactionMatcher:
    def __init__(self, mistral_client: MistralClient = None):
        self.mistral_client = mistral_client or MistralClient()

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

    def match_invoice_with_transactions(self, invoice_data: Dict[str, Any], transactions_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Trouve la meilleure correspondance entre une facture et les transactions
        """
        logger.info("Début du matching de la facture")
        logger.info(f"Données de la facture: {json.dumps(invoice_data, indent=2, default=str, ensure_ascii=False)}")
        
        # Convertir les transactions en texte
        transactions_text = "Transactions bancaires :\n"
        for _, row in transactions_df.iterrows():
            transactions_text += f"- {self._format_transaction(row)}\n"
        logger.info(f"Transactions formatées:\n{transactions_text}")

        # Préparer les données de la facture
        invoice_text = f"""Facture :
        - Date: {invoice_data['date']}
        - Montant: {invoice_data['amount']}
        - Vendeur: {invoice_data['vendor_name']}
        - Numéro: {invoice_data['invoice_number']}
        """

        prompt = f"""En tant qu'expert en rapprochement bancaire, trouve la meilleure correspondance entre cette facture et les transactions bancaires.

        {invoice_text}

        {transactions_text}

        Analyse et retourne un JSON avec :
        - match_found : boolean indiquant si une correspondance est trouvée
        - confidence_score : score de confiance entre 0 et 1
        - transaction_date : date de la transaction si trouvée
        - transaction_amount : montant de la transaction si trouvée
        - transaction_vendor : vendeur de la transaction si trouvée
        - matching_reason : explication détaillée du matching

        Retourne uniquement le JSON."""

        messages = [
            {"role": "user", "content": prompt}
        ]

        try:
            logger.info("Envoi de la requête de matching à Mistral")
            content = self.mistral_client.send_message(messages)
            
            # Nettoyer la réponse pour s'assurer qu'elle est en JSON valide
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            result = json.loads(content)
            logger.info("Matching terminé avec succès")
            logger.info(f"Résultat du matching: {json.dumps(result, indent=2, ensure_ascii=False)}")
            
            # S'assurer que tous les champs requis sont présents
            required_fields = ['match_found', 'confidence_score', 'matching_reason']
            for field in required_fields:
                if field not in result:
                    result[field] = None if field != 'match_found' else False
            
            # Ajouter les champs optionnels s'ils n'existent pas
            optional_fields = ['transaction_date', 'transaction_amount', 'transaction_vendor']
            for field in optional_fields:
                if field not in result:
                    result[field] = None
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur lors du matching: {str(e)}")
            return {
                'match_found': False,
                'confidence_score': 0.0,
                'transaction_date': None,
                'transaction_amount': None,
                'transaction_vendor': None,
                'matching_reason': f"Erreur lors de l'analyse: {str(e)}"
            } 