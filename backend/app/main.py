from fastapi import FastAPI

from app.routers import auth, catalog, members

app = FastAPI(title="Βιβλιοθήκη")

app.include_router(auth.router)
app.include_router(catalog.router)
app.include_router(members.router)


@app.get("/health")
def health():
    return {"status": "ok"}
