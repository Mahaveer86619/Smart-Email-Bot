from pydantic import BaseModel

class StructuredEmail(BaseModel):
    subject: str
    body: str
