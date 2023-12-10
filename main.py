# Erstellen der API-Routen, sowie der Logik, welche für jeden API-Call ausgeführt wird

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi .middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/hello")
def say_hello():
    return {"Nachricht1": "Hallo",
            "Nachricht2": "Das ist ein API-Call"}

@app.post("/post")
def create_value():
    return {"Message": "This is working!!"}


@app.get("/index", response_class=HTMLResponse)
def launch_index():
    with open("static/index.html", "r") as html:
        render = html.read()

    return render
