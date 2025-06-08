import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("app/core/firebase_service_account.json")

# Only initialize if not already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
