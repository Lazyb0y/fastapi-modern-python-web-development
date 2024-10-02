from pydantic import BaseModel


class Creature(BaseModel):
    name: str
    country: str
    area: str
    description: str | None = None
    aka: str
