# Agent LinkedIn : Génération des postes pour Linkedin 

Cet agent intelligent automatise la création de posts LinkedIn en utilisant l'IA pour générer du contenu pertinent et engageant. Il utilise plusieurs modèles d'IA (OpenAI, Groq, et Gemini) pour générer des posts de qualité.

## Fonctionnalités

- 🔐 Authentification sécurisée avec LinkedIn
- 🔍 Analyse des publications récentes basée sur un thème
- 🧠 Suggestions de sujets personnalisés
- ✍️ Génération de posts avec différents modèles d'IA :
  - OpenAI (GPT-4.1-mini)
  - Groq (Llama-3.3-70b-versatile)
  - Google Gemini (Gemini-2.0-flash)

## Prérequis

- Python 3.8 ou supérieur
- Compte LinkedIn
- Clés API pour :
  - OpenAI
  - Groq
  - Google Gemini

## Installation

1. Clonez ce dépôt :
```bash
git clone [URL_DU_REPO]
cd [NOM_DU_DOSSIER]
```

2. Installez les dépendances :
```bash
pip install linkedin-api
pip install openai
pip install python-dotenv
```

3. Configurez les variables d'environnement :
   - Créez un fichier `.env` à la racine du projet
   - Copiez le contenu suivant et remplissez les valeurs :
   ```
   LINKEDIN_EMAIL=your_email@example.com
   LINKEDIN_PASSWORD=your_password
   OPENAI_API_KEY=your_openai_api_key
   GROQ_API_KEY=your_groq_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```

## Utilisation

1. Lancez l'agent :
```bash
python linkedin_agent.py
```

2. Suivez les instructions à l'écran pour :
   - Vous authentifier sur LinkedIn
   - Entrer un thème pour l'analyse des publications
   - Choisir parmi les suggestions de sujets générées
   - Générer des posts avec différents modèles d'IA

## Sécurité

- Ne partagez jamais votre fichier `.env`
- Ne committez pas vos identifiants dans le code
- Utilisez des mots de passe forts
- Gardez vos clés API secrètes

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Ouvrir une issue pour signaler un bug
- Proposer une pull request pour une amélioration
- Partager vos idées d'évolution

## Licence

MIT 