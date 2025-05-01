# Projet d'Extraction de Données de Reçus par Pixtral

## 👨‍💻 Développé par

Ce projet a été réalisé dans le cadre d’un projet PRO à **HETIC** par les membres du **Groupe 6** :

- SOBGUI Ivan Joel  
- OUMAR Ben Lol  
- SGHIOURI Mohammed  
- BOTI Armel Cyrille  
- DIVENGI KIBANGUDI BUNKEMBO Nagui  

## 🔗 Liens utiles
- 💻 Application déployée : https://inovert.streamlit.app

- 🧠 Code source sur GitHub : https://github.com/sghiouri-mohammed/Bills-Fact-Matching

## Objectif du Projet

Ce projet vise à extraire automatiquement des informations clés à partir d'images de reçus ou de factures en utilisant la reconnaissance optique de caractères (Pixtral). Les informations extraites incluent typiquement la date, le montant total, la devise et le nom du vendeur. L'objectif est de simplifier la saisie de données ou la gestion des dépenses. Le script `src/server/extract_data.py` utilise le model Pixtral de Mistral qui contient le ``Computer Vision`` pour effectuer l'Pixtral et ensuite analyser le texte brut pour en extraire ces informations structurées.

## Structure du Projet

Le projet est organisé comme suit :

├── src/ # Dossier contenant le code source principal <br>
│ ├── client/ # Modules liés au client avec Streamlit  <br>
│ ├── server/ # Modules liés au backend / logique métier <br>
│ │ ├── main.py <br>
│ │ ├── extract_data.py # Logique d'extraction Pixtral via Nanonets <br>
│ │ ├── config.py # Fichier pour stocker la clé API Nanonets <br>
│ │ └── ... # Autres modules serveur possibles <br>
│ └── main.py # L'entrée principale du  fichier source <br>
├── storage # Le dossier temporaire pour upload les fichiers <br>
├── main.py # Script principal / Point d'entrée de l'application Streamlit <br>
├── requirements.txt # Liste des dépendances Python du projet <br>
├── .venv/ # Environnement virtuel Python (créé localement) <br>
└── README.md # Ce fichier d'information

## Dépendances

Lisez le requirements.txt: <a href='requirements.txt'>Pré-requis</a>


## Installation et Lancement.

Suivez ces étapes pour configurer et lancer le projet :

1.  **Cloner le dépôt** (si applicable) :
    ```bash
    git clone <url-du-depot>
    cd <nom-du-dossier-du-projet>
    ```

2.  **Créer un environnement virtuel** :
    Il est fortement recommandé d'utiliser un environnement virtuel pour isoler les dépendances du projet.
    ```bash
    python -m venv venv
    ```
    Activez l'environnement :
    *   Sur Windows :
        ```bash
        .\venv\Scripts\activate
        ```
    *   Sur macOS/Linux :
        ```bash
        source venv/bin/activate
        ```

3.  **Installer les dépendances** :
    Assurez-vous que toutes les bibliothèques nécessaires sont listées dans `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
    *(Note : Assurez-vous que `requirements.txt` contient au moins `nanonets-Pixtral` et `streamlit` si vous utilisez Streamlit).*

4.  **Configurer vos clés API et paramètres** :
    *   Changez le nom du fichier `.env.example` en `.env`.
    *   Remplacez la valeur de `MISTRAL_API_KEY` par votre propre clés.
    ```python:.env
    # Configuration de l'API Mistral
    MISTRAL_API_KEY=

    # Configuration de l'application
    DEBUG=True
    LOG_LEVEL=DEBUG

    # Configuration des timeouts
    REQUEST_TIMEOUT=30
    MAX_RETRIES=3

    # Configuration du modèle
    MISTRAL_MODEL=pixtral-12b-2409
    MAX_TOKENS=131072
    TEMPERATURE=0.0
    ```

5.  **Lancer l'application** :
    Si vous utilisez Streamlit et que `main.py` est votre point d'entrée :
    ```bash
    streamlit run main.py
    ```

    L'application devrait maintenant être accessible dans votre navigateur web à l'adresse indiquée par Streamlit (généralement `http://localhost:8501`).

## Logic et Fonctionnement de l'application

**INOVERT : Matching Automatique de Factures à un Relevé Bancaire**

Cette application a été développée pour automatiser le processus de rapprochement entre les factures et les transactions bancaires, une tâche généralement chronophage et sujette aux erreurs lorsqu'elle est réalisée manuellement.

**Comment ça fonctionne ?** <br>

Notre application utilise une technologie avancée de traitement d'images (Pixtral) et des algorithmes de matching intelligents pour :

- Extraire les données essentielles de vos factures au format image (JPG/PNG) : montants, dates, commerçants <br>
- Analyser votre relevé bancaire au format CSV <br>
- Établir automatiquement les correspondances entre chaque transaction bancaire et la facture associée <br>

**Avantages**
<br>

- Gain de temps considérable : quelques secondes suffisent pour traiter des dizaines de factures<br>
- Réduction des erreurs : notre algorithme identifie les correspondances avec précision<br>
- Interface intuitive : simple glisser ou déposer de vos fichiers<br>
- Visualisation claire des résultats et des correspondances trouvées<br>

**Confidentialité**

Vos données financières restent confidentielles et ne sont pas stockées sur nos serveurs. Tout le traitement est effectué localement dans votre navigateur.
