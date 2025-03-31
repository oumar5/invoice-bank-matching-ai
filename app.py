import streamlit as st
import pandas as pd
from services.invoice_service import InvoiceService
from components.styles import get_css
from components.header import render_header
from components.file_upload import render_file_upload, load_bank_statement
from components.results import render_results

# Configuration de la page
st.set_page_config(
    page_title="Matching Factures-Relevé Bancaire",
    page_icon="🏦",
    layout="wide"
)

# Application du style CSS
st.markdown(get_css(), unsafe_allow_html=True)

# Initialisation des services
@st.cache_resource
def get_invoice_service():
    return InvoiceService()

# Initialisation de l'état de la session
if "results" not in st.session_state:
    st.session_state.results = None
if "transactions_df" not in st.session_state:
    st.session_state.transactions_df = None

# Affichage de l'en-tête
render_header()

# Affichage des zones de téléchargement
bank_statement, invoices = render_file_upload()

# Chargement du relevé bancaire
transactions_df = load_bank_statement(bank_statement)

# Bouton de traitement
if st.button("🔍 Analyser les factures", disabled=not (bank_statement and invoices)):
    with st.spinner("Analyse en cours..."):
        try:
            # Initialisation du service
            invoice_service = get_invoice_service()
            
            # Préparation des données pour le traitement
            invoice_contents = [
                {
                    'name': invoice.name,
                    'content': invoice.getvalue()
                }
                for invoice in invoices
            ]
            
            # Traitement des factures
            results = invoice_service.process_all(
                bank_statement.getvalue(),
                invoice_contents
            )
            
            # Stockage des résultats dans l'état de la session
            st.session_state.results = results
            st.session_state.transactions_df = transactions_df
            
            st.success("✅ Analyse terminée avec succès !")
        except Exception as e:
            st.error(f"❌ Une erreur est survenue : {str(e)}")

# Affichage des résultats
if st.session_state.results is not None and st.session_state.transactions_df is not None and not st.session_state.transactions_df.empty:
    render_results(st.session_state.results, st.session_state.transactions_df) 