import uvicorn
from fastapi import FastAPI


def create_app():
    app = FastAPI()

    return app


app = create_app()


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
