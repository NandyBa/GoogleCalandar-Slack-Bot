import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from datetime import datetime
from dateutil.relativedelta import relativedelta

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


	def récupérér_les_prochains_évènements(self, calendarId='primary', nombre_d_évènements=10):
		"""
			Permet de récupérer les i prochains évènements
			d'un calendrier.
		"""
		now = datetime.datetime.utcnow()
		timeMin = now.isoformat() + 'Z' # 'Z' indicates UTC time

		events_result = self.service.events().list(
				calendarId=calendarId,
				timeMin=timeMin,
				maxResults=nombre_d_évènements, singleEvents=True,
				orderBy='startTime'
			).execute()

		events = events_result.get('items', [])

		return events

	def récupérér_les_évènements_ayant_lieu_à_cette_date(self, date, calendarId='primary'):

		date = datetime.strptime(date, '%d/%m/%Y')

		timeMin = date.isoformat() + 'Z' # 'Z' indicates UTC time
		timeMax = ( date + relativedelta(days=1) ).isoformat() + 'Z' # 'Z' indicates UTC time

		print('Getting the upcoming 10 events')
		
		events_result = self.service.events().list(
				calendarId=calendarId,
				timeMin=timeMin,
				timeMax=timeMax,
				singleEvents=True,
				orderBy='startTime'
			).execute()

		events = events_result.get('items', [])

		return events

	def récupérér_les_évènements_ayant_lieu_aujourdhui(self, calendarId='primary'):
		aujourd_hui = datetime.now()
		aujourd_hui = aujourd_hui.strftime("%d/%m/%Y")
		return self.récupérér_les_évènements_ayant_lieu_à_cette_date(aujourd_hui)

	
	def récupérer_la_listes_des_calendriers(self):
		calendriers = []
		page_token = None
		while True:
			calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
			for calendar_list_entry in calendar_list['items']:
				calendriers.append(calendar_list_entry)
				page_token = calendar_list.get('nextPageToken')
			if not page_token:
				break
		return calendriers