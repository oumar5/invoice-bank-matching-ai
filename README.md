# 🏦 Matching Factures-Relevé Bancaire

Une application Streamlit qui utilise l'IA pour analyser automatiquement vos factures et les faire correspondre avec votre relevé bancaire.

## 📋 Fonctionnalités

- 📄 Analyse automatique des factures (JPG, JPEG, PNG)
- 🏦 Intégration avec les relevés bancaires (CSV)
- 🔍 Matching intelligent avec score de confiance
- 📊 Visualisation des résultats
- 🎨 Interface utilisateur moderne et intuitive

## 🛠️ Structure du Projet

```
invoice-bank-matching-ai/
├── app.py                 # Application principale Streamlit
├── components/           # Composants de l'interface utilisateur
│   ├── header.py        # En-tête de l'application
│   ├── file_upload.py   # Gestion du téléchargement des fichiers
│   ├── results.py       # Affichage des résultats
│   └── styles.py        # Styles CSS personnalisés
├── services/            # Services métier
│   ├── api/            # Services d'API
│   │   ├── mistral_client.py
│   │   ├── invoice_analyzer.py
│   │   └── transaction_matcher.py
│   ├── utils/          # Utilitaires
│   │   └── logging_config.py
│   └── invoice_service.py
├── models/             # Modèles de données
│   └── data_models.py
└── config/            # Configuration
    └── settings.py
```

## 🚀 Installation

1. Clonez le repository :
```bash
git clone https://github.com/votre-username/invoice-bank-matching-ai.git
cd invoice-bank-matching-ai
```

2. Créez un environnement virtuel et activez-le :
```bash
conda create -n invoice python=3.9
conda activate invoice
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurez votre clé API Mistral :
```bash
export MISTRAL_API_KEY=votre_clé_api
```

## 💻 Utilisation

1. Lancez l'application :
```bash
streamlit run app.py
```

2. Téléchargez votre relevé bancaire au format CSV
3. Téléchargez une ou plusieurs factures (JPG, JPEG, PNG)
4. Cliquez sur "Analyser les factures"
5. Consultez les résultats et les correspondances trouvées

## 🎨 Interface Utilisateur

L'application est divisée en plusieurs composants :

- **En-tête** : Présente le titre et la description de l'application
- **Téléchargement de fichiers** : Permet de télécharger le relevé bancaire et les factures
- **Résultats** : Affiche les métriques globales et les détails des correspondances

## 🔧 Configuration

Les paramètres de configuration sont stockés dans `config/settings.py` :
- Configuration de l'API Mistral
- Paramètres de logging
- Configuration des requêtes API

## 📝 Logs

Les logs sont configurés dans `services/utils/logging_config.py` et incluent :
- Niveau de log : INFO
- Format : `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- Sortie : Console

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- [Streamlit](https://streamlit.io/) pour le framework d'interface utilisateur
- [Mistral AI](https://mistral.ai/) pour l'API d'analyse
- [Pandas](https://pandas.pydata.org/) pour le traitement des données