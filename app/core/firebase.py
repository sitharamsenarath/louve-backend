import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("app/core/firebase_service_account.json")
firebase_admin.initialize_app(cred)
