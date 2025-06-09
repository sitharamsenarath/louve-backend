from pydantic import BaseModel

class FirebaseSyncRequest(BaseModel):
    name: str | None = None
