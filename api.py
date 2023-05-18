import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/test")
def root(name: str):
    return {"test": "test" + name }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)