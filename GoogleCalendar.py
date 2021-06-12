import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class GoogleCalendar():
	"""
		Classe permettant d'intéragir avec l'API de Google Calendar
	"""
	def __init__(self):
		# Si le scopes est modifié il est nécessaire de supprimer le fichier token.json
		SCOPES = ['https://www.googleapis.com/auth/calendar']

		creds = None
		# Un token de connexion se crée automatiquement à la connection de l'utilisateur 
		# et ce regénère régulièrement de façon automatique 
		if os.path.exists('token.json'):
			creds = Credentials.from_authorized_user_file('token.json', SCOPES)
		# Si les credentials n'existes pas ou si elles ne contienent pas la clée "valid"
		# on demande à l'utilisateur de se ré-enregistrer
		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
					'credentials.json', SCOPES)
				creds = flow.run_local_server(port=0)
			# On sauvegarde les credentials en vu des prochaines connexions
			with open('token.json', 'w') as token:
				token.write(creds.to_json())

		self.service = build('calendar', 'v3', credentials=creds)
