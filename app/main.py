# Erstellen der API-Routen, sowie der Logik, welche für jeden API-Call ausgeführt wird
import os
import subprocess

from datetime import datetime

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from fastapi.responses import HTMLResponse
from fastapi .middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.models import Base
from app import crud
from app import schemas

Base.metadata.create_all(bind=engine)

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

test_host = "localhost"
live_host = "172.20.174.121"
client1_address = "127.0.0.1"
client2_address = ""


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
    return {"Nachricht1": "Hallo!",
            "Nachricht2": "Das ist ein API-Call",
            "Nachricht3": "Wie geht es dir?"}


# noinspection PyTypeChecker
@app.post("/api/v1/new-temperatures")
def create_new_temperatures(temp_c: float, temp_f: float, client: str, db: Session = Depends(get_db)):
    return crud.create_reading(db, temp_c, temp_f, client)


@app.get("/api/v1/all-temperatures")
def get_all_temperatures(db: Session = Depends(get_db)):
    return crud.get_all_readings(db)


@app.get("/api/v1/last-reading")
def get_id_in_order(db: Session = Depends(get_db)):
    return crud.get_last_reading(db)


@app.get("/api/v1/temperature/{id}", response_model=schemas.Temperature)
def get_both_temperatures_by_id(id: int, db: Session = Depends(get_db)):
    return crud.read_by_id(db, id)


@app.get("/api/v1/temerature/{id}")
def get_temperature_by_id(id: int, is_celsius: bool, db: Session = Depends(get_db)):
    return crud.read_reading_Temperature(db, id, is_celsius)


@app.get("/api/v1/get-temps-from-client")
def get_all_temperatures_from_client(client: str, db: Session = Depends(get_db)):
    return crud.read_reading_by_client(db, client)


@app.get("/api/v1/get-temps-from-client-and-time")
def get_temperature_by_client_and_time(time: datetime, client: str, db: Session = Depends(get_db)):
    return crud.read_reading_by_Client_and_Time(db, client, time)


@app.put("/api/v1/update_temperature_of_id")
def update_temperature_of_id(temp_c: float, temp_f: float, id: int, db: Session = Depends(get_db)):
    return crud.update_reading(db, id, temp_c, temp_f)


@app.delete("/api/v1/delete-temperature")
def delete_temperature_of_id(id: int, db: Session = Depends(get_db)):
    return crud.delete_reading(db, id)


@app.get("/index", response_class=HTMLResponse)
def launch_index():
    rpi_1 = subprocess.run(["ping", "-n", "1", "172.20.105.186"], capture_output=True)
    rpi_1_out = rpi_1.stdout
    print(rpi_1_out)
    with open("static/index.html", "r") as html:
        render = html.read()

    return render


@app.get("/get-temps-in-timeframe")
def get_temps_in_timeframe(start: datetime = datetime.now(), end: datetime = datetime.now(), db: Session = Depends(get_db)):
    data = crud.get_reading_by_timeframe(db, start, end)
    return data


@app.get("/get-uptime")
def get_uptime():
    host_os = os.name
    print(host_os)
    rpi_1 = subprocess.run(["ping", "-n", "1", "172.20.191.79"], capture_output=True)
    rpi_1_out = rpi_1.stdout
    print(rpi_1_out)
    if "Empfangen = 1" in str(rpi_1_out):
        rpi1_up = True
    else:
        rpi1_up = False

    return rpi1_up


@app.get("/graph-view", response_class=HTMLResponse)
def graph_view():
    with open("static/diagramm.html", "r") as html:
        render = html.read()

    return render
