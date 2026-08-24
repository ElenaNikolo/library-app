from fastapi import FastAPI

from app.routers import auth, catalog, loans, members, users

app = FastAPI(title="Βιβλιοθήκη")

app.include_router(auth.router)
app.include_router(catalog.router)
app.include_router(loans.router)
app.include_router(members.router)
app.include_router(users.router)


@app.get("/health")
def health():
    return {"status": "ok"}
