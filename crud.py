# CRUD Anweisungen für unsere Datenbankabfragen

from sqlalchemy.orm import Session, Query
from datetime import datetime
from . import models, schemas


def create_reading(db: Session, id: int, temp_c: float, temp_f: float, client: str):
    new_data = models.Readings(id=id, temp_c=temp_c, temp_f=temp_f, client=client, time=datetime.now())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data

def create_reading(db: Sesssion, c: bool):
    # if c -> celsius

def read_reading(db: Session):
    # Alles bzw. Ganze Tabelle

def read_reading(db: Session, id: int, c: bool):
    # nur Celsius o. Fahrenheit

def read_reading(db: Session, id: int):
    # Id

def read_reading(db: Session, client: str, time: datetime):
    # Client und Zeit

def update_reading():
    # Alles bzw. Ganze Tabelle
    # Id
    # Client und Zeit

def delete_reading():
    # Alles bzw. Ganze Tabelle
    # Id
    # Client und Zeit