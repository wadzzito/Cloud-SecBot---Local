from fastapi import FastAPI
from db.database import init_db
from routes import findings, actions

app = FastAPI(title="Cloud SecBot API")

init_db()

app.include_router(findings.router)
app.include_router(actions.router)

@app.get("/")
def root():
    return {"status": "Cloud SecBot API corriendo"}