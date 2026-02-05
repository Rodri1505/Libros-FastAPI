from pydantic import BaseModel
from datetime import date

class Libro(BaseModel):
    id: int | None = None
    titulo: str | None = None
    autor: str | None = None
    fecha_publicacion: date | None = None
    digital: bool | None = None
