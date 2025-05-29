# pip install linkedin-api
# pip install google-auth google-auth-oauthlib google-auth-httplib2
# pip install google-api-python-client
# pip install openai



import os
import json
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import openai
from datetime import datetime
import requests
from urllib.parse import urlencode
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import sys
import time
from IPython.display import Markdown, display
from openai import OpenAI


class LinkedInAgent:
    def __init__(self):
        print("Initialisation de LinkedInAgent...")
            
        try:
            load_dotenv()
            print("Variables d'environnement chargées")
            
            # Vérification des variables d'environnement
            required_vars = ['OPENAI_API_KEY', 'GOOGLE_API_KEY', 'GROQ_API_KEY', 'LINKEDIN_EMAIL', 'LINKEDIN_PASSWORD']
            missing_vars = [var for var in required_vars if not os.getenv(var) or os.getenv(var) == f'your_{var.lower()}']
            
            if missing_vars:
                print("\nErreur : Variables d'environnement manquantes ou non configurées :")
                for var in missing_vars:
                    print(f"- {var}")
                print("\nVeuillez configurer ces variables dans le fichier .env")
                sys.exit(1)
            
            print("Configuration des clients...")
            self.google_docs_service = None
            
            # Configuration OpenAI
            print("Configuration du client OpenAI...")
            try:
                self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
                # Test de la connexion OpenAI
                self.openai_client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "user", "content": "test"}],
                )
                print("Connexion à OpenAI réussie")
            except Exception as e:
                print(f"Erreur lors de la connexion à OpenAI : {str(e)}")
                raise
            
            # Configuration LinkedIn
            print("Configuration du client LinkedIn...")
            try:
                self.linkedin_email = os.getenv('LINKEDIN_EMAIL')
                self.linkedin_password = os.getenv('LINKEDIN_PASSWORD')
                print("Identifiants LinkedIn chargés")
            except Exception as e:
                print(f"Erreur lors de la configuration de LinkedIn : {str(e)}")
                raise
            
            print("Initialisation terminée avec succès")
        except Exception as e:
            print(f"\nErreur lors de l'initialisation : {str(e)}")
            sys.exit(1)

    def authenticate_linkedin(self):
        """Authentifie l'utilisateur sur LinkedIn"""
        try:
            print("Tentative de connexion à LinkedIn...")
            # La logique d'authentification LinkedIn
            # Pour l'instant, nous simulons une connexion réussie
            print("Connexion à LinkedIn simulée")
            return True
        except Exception as e:
            print(f"Erreur lors de l'authentification sur LinkedIn : {str(e)}")
            return False

    def analyze_recent_posts(self):
        """Analyse les publications récentes de l'utilisateur"""
        try:
            print("Analyse des publications récentes...")
            # Simulation d'une analyse
            print("Entrez un thème qui décrit le mieux votre domaine d'intérêt")
            theme = input()
            request = f"Analyse efficacement toutes les publications récentes autour de {theme} sur LinkedIn."
            request += " Compare les publications avec les tendances actuelles."
            request += " Pour les publications qui sont en adéquation avec les tendances actuelles, énumère trois thèmes différents qui cadrent bien avec ces publications."
            request += " Je veux uniquement les thèmes."
            messages = [{"role": "user", "content": request}]
            openai = OpenAI()
            response = openai.chat.completions.create(model="gpt-4.1-mini", messages=messages)
            answer = response.choices[0].message.content

            print(answer)

            return {
                'themes': answer
            }
        except Exception as e:
            print(f"Erreur lors de l'analyse des publications : {str(e)}")
            return None

    def generate_topic_suggestions(self, analysis):
        """Génère des suggestions de sujets basées sur l'analyse"""
        try:
            print("Génération des suggestions avec OpenAI...")
            response = self.openai_client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "Tu es un expert en contenu LinkedIn."},
                    {"role": "user", "content": f"Génère 5 suggestions de sujets pertinents basées sur cette analyse : {analysis}"}
                ]
            )
            suggestions = response.choices[0].message.content.split('\n')
            print("Génération des suggestions terminée")
            return suggestions
        except Exception as e:
            print(f"Erreur lors de la génération des suggestions : {str(e)}")
            return []

    def generate_posts(self, topic):
        """Génère des posts LinkedIn sur le sujet choisi"""
        
        posts = {}
        try:
            print(f"Génération des posts sur le sujet : {topic}")
            
            # Message 
            messages=[
                {"role": "system", "content": "Tu es un expert en rédaction de posts LinkedIn."},
                {"role": "user", "content": f"Génère un post LinkedIn sur le sujet : {topic}. Inclus un appel à l'action à la fin du post."}
            ]
            
            # OpenAI model
            model_name = "gpt-4.1-mini"
            response = self.openai_client.chat.completions.create(
                model=model_name,
                messages=messages
            )
            post = response.choices[0].message.content.split('\n\n')
            print(f"Génération du post terminée pour {model_name}")
            posts[model_name] = post
            
            # Groq model
            groq_api_key = os.getenv('GROQ_API_KEY')
            if groq_api_key:
                try:
                    groq = OpenAI(
                        api_key=groq_api_key,
                        base_url="https://api.groq.com/openai/v1"
                    )
                    model_name = "llama-3.3-70b-versatile"
                    response = groq.chat.completions.create(
                        model=model_name,
                        messages=messages
                    )
                    post = response.choices[0].message.content.split('\n\n')
                    print(f"Génération du post terminée pour {model_name}")
                    posts[model_name] = post
                except Exception as e:
                    print(f"Erreur lors de la génération avec Groq : {str(e)}")
            
            # Google Gemini model
            google_api_key = os.getenv('GOOGLE_API_KEY')
            if google_api_key:
                try:
                    gemini = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
                    model_name = "gemini-2.0-flash"
                    response = gemini.chat.completions.create(
                        model=model_name,
                        messages=messages
                    )
                    post = response.choices[0].message.content.split('\n\n')
                    print(f"Génération du post terminée pour {model_name}")
                    posts[model_name] = post
                except Exception as e:
                    print(f"Erreur lors de la génération avec Gemini : {str(e)}")
            
            return posts
        except Exception as e:
            print(f"Erreur lors de la génération des posts : {str(e)}")
            return {}

def main():
    try:
        print("Démarrage du programme...")
        agent = LinkedInAgent()
        
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
            if len(suggestion) > 0 and suggestion[0].isdigit(): # Vérifie si le premier élément est un entier
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
    
    
    