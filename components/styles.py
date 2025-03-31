def get_css():
    return """
    <style>
    /* Variables de couleur */
    :root {
        --primary-color: #0d6efd;
        --primary-hover: #0b5ed7;
        --text-color: #000000;
        --bg-color: #e9ecef;
        --component-bg: #ffffff;
        --border-color: #dee2e6;
        --shadow-color: rgba(0,0,0,0.1);
    }
    
    /* Fond principal */
    .stApp {
        background-color: var(--bg-color) !important;
    }
    .main {
        background-color: var(--bg-color) !important;
        padding: 2rem;
        min-height: 100vh;
    }
    
    /* Style du texte */
    .stMarkdown {
        color: var(--text-color) !important;
    }
    .stMarkdown p {
        color: var(--text-color) !important;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--primary-color) !important;
    }
    
    /* Labels des zones de dépôt */
    .stFileUploader label {
        color: var(--text-color) !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
    .stFileUploader .stMarkdown {
        color: var(--text-color) !important;
    }
    .stFileUploader .stMarkdown p {
        color: var(--text-color) !important;
    }
    .stFileUploader .stMarkdown strong {
        color: var(--text-color) !important;
    }
    
    /* Boutons */
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
        background-color: var(--primary-color);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: var(--primary-hover);
    }
    
    /* Métriques */
    .stMetric {
        background-color: var(--component-bg);
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
        box-shadow: 0 2px 4px var(--shadow-color);
        border: 1px solid var(--border-color);
    }
    .stMetric [data-testid="stMetricValue"] {
        color: var(--primary-color) !important;
    }
    .stMetric [data-testid="stMetricLabel"] {
        color: var(--text-color) !important;
    }
    
    /* Expandeurs */
    .stExpander {
        background-color: var(--component-bg);
        border-radius: 5px;
        box-shadow: 0 2px 4px var(--shadow-color);
        margin-bottom: 1rem;
        border: 1px solid var(--border-color);
    }
    .stExpander .streamlit-expanderHeader {
        color: var(--primary-color) !important;
        font-weight: bold;
    }
    
    /* Zone de dépôt de fichiers */
    .stFileUploader {
        background-color: var(--component-bg);
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid var(--border-color);
        box-shadow: 0 2px 4px var(--shadow-color);
    }
    .uploadedFile {
        background-color: var(--bg-color);
        border: 1px solid var(--border-color);
        border-radius: 5px;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    
    /* Messages */
    .stSuccess {
        background-color: #d1e7dd;
        border: 1px solid #badbcc;
        color: #0f5132;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px var(--shadow-color);
    }
    .stError {
        background-color: #f8d7da;
        border: 1px solid #f5c2c7;
        color: #842029;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px var(--shadow-color);
    }
    .stWarning {
        background-color: #fff3cd;
        border: 1px solid #ffecb5;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px var(--shadow-color);
    }
    
    /* Spinner */
    .stSpinner {
        color: var(--primary-color);
    }
    
    /* Sous-titres */
    .stSubheader {
        color: var(--primary-color) !important;
        font-weight: bold;
    }
    
    /* Texte en gras */
    strong {
        color: var(--text-color) !important;
    }
    
    /* Liens */
    a {
        color: var(--primary-color) !important;
    }
    
    /* Texte dans les JSON */
    .stJson {
        color: var(--text-color) !important;
    }
    
    /* Texte dans les tooltips */
    .stTooltip {
        color: var(--text-color) !important;
    }
    
    /* Texte dans les messages d'aide */
    .stHelp {
        color: var(--text-color) !important;
    }
    
    /* Style global pour tous les composants */
    .stMarkdown, .stButton, .stMetric, .stExpander, .stFileUploader, 
    .stSuccess, .stError, .stWarning, .stSpinner, .stSubheader, 
    .stJson, .stTooltip, .stHelp {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    /* Forcer le fond de l'application */
    .stApp > div {
        background-color: var(--bg-color) !important;
    }
    
    /* Forcer le fond des conteneurs */
    .stApp > div > div {
        background-color: var(--bg-color) !important;
    }
    
    /* Forcer le fond des sections */
    .stApp > div > div > div {
        background-color: var(--bg-color) !important;
    }
    </style>
    """ 