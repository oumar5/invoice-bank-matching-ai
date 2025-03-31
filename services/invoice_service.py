import pandas as pd
from io import BytesIO
from typing import Dict, Any, List
from services.api.invoice_analyzer import InvoiceAnalyzer
from services.api.transaction_matcher import TransactionMatcher
from services.utils.logging_config import setup_logger

logger = setup_logger('InvoiceService')

class InvoiceService:
    def __init__(self):
        self.analyzer = InvoiceAnalyzer()
        self.matcher = TransactionMatcher()

    def process_all(self, bank_statement_content: bytes, invoice_contents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Traite l'ensemble des factures et trouve les correspondances
        """
        logger.info(f"Début du traitement de {len(invoice_contents)} factures")
        
        # Charger le relevé bancaire
        transactions_df = pd.read_csv(BytesIO(bank_statement_content))
        logger.info(f"Relevé bancaire chargé avec {len(transactions_df)} transactions")
        logger.info(f"Colonnes du relevé: {list(transactions_df.columns)}")
        logger.info(f"Premières lignes du relevé:\n{transactions_df.head().to_string()}")
        
        # Traiter chaque facture
        results = []
        for i, invoice_content in enumerate(invoice_contents, 1):
            logger.info(f"Traitement de la facture {i}/{len(invoice_contents)}: {invoice_content['name']}")
            
            # Analyser la facture
            invoice_data = self.analyzer.analyze(invoice_content['content'])
            
            # Trouver les correspondances
            match_result = self.matcher.match_invoice_with_transactions(invoice_data, transactions_df)
            
            # Combiner les résultats
            result = {
                'filename': invoice_content['name'],
                'invoice_data': invoice_data,
                'match_result': match_result
            }
            results.append(result)
            
            logger.info(f"Facture {i} traitée avec succès")
        
        logger.info("Traitement de toutes les factures terminé")
        final_result = {
            'results': results,
            'transactions': transactions_df.to_dict('records')
        }
        return final_result 