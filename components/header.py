import streamlit as st

def render_header():
    st.title("🏦 Matching Factures-Relevé Bancaire")
    st.markdown("""
    Cette application permet de :
    - Analyser automatiquement vos factures
    - Les faire correspondre avec les transactions de votre relevé bancaire
    - Afficher les résultats avec un score de confiance
    """) 