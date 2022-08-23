from pydantic import BaseModel


class Calculator(BaseModel):
    id: int
    button: str
