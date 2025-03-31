import streamlit as st
import pandas as pd
from typing import Dict, Any, List

def render_results(results: Dict[str, Any], transactions_df: pd.DataFrame) -> None:
    """
    Affiche les résultats de l'analyse des factures
    """
    st.subheader("📊 Résultats")
    
    # Métriques globales
    total_invoices = len(results["results"])
    matched_invoices = sum(1 for r in results["results"] if r["match_result"]["match_found"])
    match_rate = (matched_invoices / total_invoices * 100) if total_invoices > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total des factures", total_invoices)
    with col2:
        st.metric("Factures correspondantes", matched_invoices)
    with col3:
        st.metric("Taux de correspondance", f"{match_rate:.1f}%")
    
    # Détails des correspondances
    st.subheader("🔍 Détails des correspondances")
    
    for result in results["results"]:
        with st.expander(f"📄 {result['filename']}", expanded=True):
            # Informations de la facture
            invoice_data = result["invoice_data"]
            st.markdown("**Informations de la facture :**")
            st.markdown(f"- Date : {invoice_data['date']}")
            st.markdown(f"- Montant : {invoice_data['amount']}")
            st.markdown(f"- Vendeur : {invoice_data['vendor_name']}")
            st.markdown(f"- Numéro : {invoice_data['invoice_number']}")
            
            # Résultat du matching
            match_result = result["match_result"]
            if match_result["match_found"]:
                st.success(f"✅ Correspondance trouvée (Score de confiance : {match_result['confidence_score']:.2f})")
                st.markdown(f"**Raison de la correspondance :** {match_result['matching_reason']}")
                
                # Afficher la transaction correspondante
                if match_result["transaction_date"] and match_result["transaction_amount"]:
                    matching_transaction = transactions_df[
                        (transactions_df['date'] == match_result["transaction_date"]) &
                        (transactions_df['amount'] == match_result["transaction_amount"])
                    ]
                    
                    if not matching_transaction.empty:
                        st.markdown("**Transaction correspondante :**")
                        st.dataframe(matching_transaction)
            else:
                st.warning("⚠️ Aucune correspondance trouvée")
            
            # Texte brut extrait
            st.markdown("**📝 Texte brut extrait :**")
            st.text(invoice_data.get('raw_text', 'Aucun texte extrait')) 