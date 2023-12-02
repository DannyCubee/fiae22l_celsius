# Erstellen der API-Routen, sowie der Logik, welche für jeden API-Call ausgeführt wird

from fastapi import FastAPI
import models


from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/neue_auslesung")
def say_hello():
    return {"Nachricht1": "Hallo",
            "Nachricht2": "Das ist ein API-Call"}

