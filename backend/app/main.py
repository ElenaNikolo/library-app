from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, catalog, loans, members, requests, users

app = FastAPI(title="Βιβλιοθήκη")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(catalog.router)
app.include_router(loans.router)
app.include_router(members.router)
app.include_router(requests.router)
app.include_router(users.router)


@app.get("/health")
def health():
    return {"status": "ok"}
