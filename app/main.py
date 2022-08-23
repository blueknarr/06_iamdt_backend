import uvicorn

from app.api import calculator
from fastapi import FastAPI


def create_app():
    app = FastAPI()

    app.include_router(
        calculator.router, tags=["calculator"], prefix="/api/v1/calculator"
    )

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
