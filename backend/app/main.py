from fastapi import FastAPI

app = FastAPI(title="Βιβλιοθήκη")


@app.get("/health")
def health():
    return {"status": "ok"}
