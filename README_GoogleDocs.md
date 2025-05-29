# Agent LinkedIn : Génération et Sauvegarde avec Google Docs

Cet agent intelligent automatise la création de posts LinkedIn en utilisant l'IA pour générer du contenu pertinent et engageant, et les sauvegarde automatiquement dans Google Docs. Il inclut également la possibilité d'une publication assistée sur LinkedIn.

## Fonctionnalités

- 🔐 Authentification sécurisée avec LinkedIn et Google
- 🔍 Analyse des publications récentes
- 🧠 Suggestions de sujets personnalisés
- ✍️ Génération de posts avec différents styles (via OpenAI, Groq, Gemini)
- 📄 Sauvegarde automatique dans Google Docs
- ✅ Publication assistée sur LinkedIn (fonctionnalité potentielle / à venir)

## Prérequis

- Python 3.8 ou supérieur
- Compte LinkedIn
- Compte Google avec accès à Google Docs
- Clés API pour OpenAI, Groq et/ou Google Gemini

## Installation

1. Clonez ce dépôt :
```bash
git clone [URL_DU_REPO]
cd [NOM_DU_DOSSIER]
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurez les variables d'environnement :
   - Créez un fichier `.env` à la racine du projet
   - Copiez le contenu suivant et remplissez les valeurs :
   ```
   LINKEDIN_EMAIL=your_email@example.com
   LINKEDIN_PASSWORD=your_password
   OPENAI_API_KEY=your_openai_api_key
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   GOOGLE_API_KEY=your_google_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

4. Configurez l'authentification Google :
   - Allez sur [Google Cloud Console](https://console.cloud.google.com)
   - Créez un nouveau projet
   - Activez l'API Google Docs
   - Créez des identifiants OAuth 2.0 (type "Desktop app" ou "Application de bureau")
   - Téléchargez le fichier `credentials.json` et placez-le à la racine du projet. Ce fichier contient les informations d'identification de votre application.

## Utilisation

1. Lancez l'agent :
```bash
python linkedin_agent_with_docs.py
```

2. Suivez les instructions à l'écran pour :
   - Vous authentifier
   - Choisir un sujet
   - Générer et sauvegarder les posts dans Google Docs

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