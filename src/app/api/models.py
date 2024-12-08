from pydantic import BaseModel, Field
from datetime import datetime as dt


class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)
    completed: str = "False"
    created_date: str = dt.now().strftime("%Y-%m-%d %H:%M")


class NoteDB(NoteSchema):
    id: int
