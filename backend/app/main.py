from fastapi import FastAPI

from app.routers import auth, catalog

app = FastAPI(title="Βιβλιοθήκη")

app.include_router(auth.router)
app.include_router(catalog.router)


@app.get("/health")
def health():
    return {"status": "ok"}
