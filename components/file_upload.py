import streamlit as st
import pandas as pd
from typing import Tuple, Optional

def render_file_upload() -> Tuple[Optional[bytes], Optional[list]]:
    """
    Affiche les zones de téléchargement de fichiers et retourne les fichiers téléchargés.
    """
    st.subheader("📤 Téléchargement des fichiers")
    
    # Zone de dépôt pour le relevé bancaire
    bank_statement = st.file_uploader(
        "🏦 Relevé bancaire (CSV)",
        type=["csv"],
        help="Téléchargez votre relevé bancaire au format CSV"
    )
    
    # Zone de dépôt pour les factures
    invoices = st.file_uploader(
        "📄 Factures (JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        help="Téléchargez une ou plusieurs factures au format JPG, JPEG ou PNG"
    )
    
    return bank_statement, invoices

def load_bank_statement(bank_statement) -> Optional[pd.DataFrame]:
    """
    Charge le relevé bancaire dans un DataFrame.
    """
    if bank_statement is not None:
        try:
            df = pd.read_csv(bank_statement)
            st.success(f"✅ Relevé bancaire chargé avec succès ({len(df)} transactions)")
            return df
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement du relevé bancaire : {str(e)}")
            return None
    return None 