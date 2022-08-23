from app.schemas.calculator import Calculator
from fastapi import APIRouter


router = APIRouter()
calculator_db: dict = {}


@router.get("/")
def read_item():
    return {"hello": "world"}
