# pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

import os
from linkedin_agent import LinkedInAgent
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

class LinkedInAgentWithDocs(LinkedInAgent):
    def __init__(self):
        super().__init__()
        self.SCOPES = ['https://www.googleapis.com/auth/documents']
        self.creds = None
        self.docs_service = None
        self.initialize_google_docs()

    def initialize_google_docs(self):
        """Initialise la connexion à Google Docs"""
        try:
            print("Initialisation de Google Docs...")
            if os.path.exists('token.json'):
                self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
            
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', self.SCOPES)
                    self.creds = flow.run_local_server(port=0)
                
                with open('token.json', 'w') as token:
                    token.write(self.creds.to_json())

            self.docs_service = build('docs', 'v1', credentials=self.creds)
            print("Connexion à Google Docs établie")
        except Exception as e:
            print(f"Erreur lors de l'initialisation de Google Docs : {str(e)}")
            raise

    def create_new_document(self, title):
        """Crée un nouveau document Google Docs"""
        try:
            document = {
                'title': title
            }
            doc = self.docs_service.documents().create(body=document).execute()
            print(f"Document créé avec l'ID : {doc.get('documentId')}")
            return doc.get('documentId')
        except HttpError as error:
            print(f"Erreur lors de la création du document : {error}")
            return None

    def append_to_document(self, document_id, content):
        """Ajoute du contenu à un document Google Docs"""
        try:
            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': 1
                        },
                        'text': f"\n{content}\n"
                    }
                }
            ]
            self.docs_service.documents().batchUpdate(
                documentId=document_id,
                body={'requests': requests}
            ).execute()
            print("Contenu ajouté au document")
        except HttpError as error:
            print(f"Erreur lors de l'ajout du contenu : {error}")

    def save_posts_to_docs(self, posts, topic):
        """Sauvegarde les posts générés dans un document Google Docs"""
        try:
            # Créer un nouveau document avec la date et le sujet
            date_str = datetime.now().strftime("%Y-%m-%d")
            title = f"Posts LinkedIn - {topic} - {date_str}"
            document_id = self.create_new_document(title)
            
            if not document_id:
                return False

            # Ajouter un en-tête
            header = f"Posts LinkedIn générés le {date_str}\nSujet : {topic}\n\n"
            self.append_to_document(document_id, header)

            # Ajouter les posts de chaque modèle
            for model_name, post_list in posts.items():
                model_header = f"\nPosts générés par {model_name}:\n"
                self.append_to_document(document_id, model_header)
                
                for i, post in enumerate(post_list, 1):
                    post_content = f"\nPost {i}:\n{post}\n"
                    self.append_to_document(document_id, post_content)

            print(f"Les posts ont été sauvegardés dans le document : {title}")
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des posts : {str(e)}")
            return False

def main():
    try:
        print("Démarrage du programme...")
        agent = LinkedInAgentWithDocs()
        
        # Authentification LinkedIn
        print("\nTentative d'authentification sur LinkedIn...")
        if not agent.authenticate_linkedin():
            print("Échec de l'authentification sur LinkedIn")
            return
        
        # Analyse des posts récents
        print("\nAnalyse des publications récentes...")
        analysis = agent.analyze_recent_posts()
        if not analysis:
            print("Impossible d'analyser les publications récentes")
            return
        
        # Génération des suggestions
        print("\nGénération des suggestions de sujets...")
        suggestions = agent.generate_topic_suggestions(analysis)
        print("\nSuggestions de sujets :")
        
        num_suggestion = []
        for suggestion in suggestions:
            if len(suggestion) > 0 and suggestion[0].isdigit():
                num_suggestion.append(suggestion)
        print(num_suggestion)
        
        # Boucle principale
        compt = 1
        while True:
            if compt == 1:
                choice = input("\nChoisissez un numéro de suggestion ou entrez votre propre sujet (ou 'q' pour quitter) : ")
            else:
                choice = input("\nChoisissez un nouveau numéro de suggestion ou entrez votre propre sujet (ou 'q' pour quitter) : ")
            
            if choice.lower() == 'q':
                break
                
            try:
                topic = num_suggestion[int(choice) - 1] if choice.isdigit() else choice
                posts = agent.generate_posts(topic)
                
                # Sauvegarder les posts dans Google Docs
                if agent.save_posts_to_docs(posts, topic):
                    print("\nPosts générés et sauvegardés avec succès!")
                else:
                    print("\nErreur lors de la sauvegarde des posts")
                
                print("\nPosts générés :")
                for model_name, post_list in posts.items():
                    print(f"\nPosts générés par {model_name} :")
                    for i, post in enumerate(post_list, 1):
                        print(f"{i}. {post}")
                compt += 1
            except Exception as e:
                print(f"Une erreur est survenue : {str(e)}")
                continue
    except Exception as e:
        print(f"Erreur critique: {str(e)}")
        return

if __name__ == "__main__":
    main() 