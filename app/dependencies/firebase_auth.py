from fastapi import Header, HTTPException, Depends
from firebase_admin import auth as firebase_auth

def verify_firebase_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    id_token = authorization.split(" ")[1]

    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        return decoded_token  # includes uid, email, name, etc.
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")
