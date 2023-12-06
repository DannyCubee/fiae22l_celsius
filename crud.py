# CRUD Anweisungen für unsere Datenbankabfragen

from sqlalchemy.orm import Session, Query
from datetime import datetime
from . import models, schemas


def create_reading(db: Session, id: int, temp_c: float, temp_f: float, client: str):
    new_data = models.Readings(
        id=id,
        temp_c=temp_c,
        temp_f=temp_f,
        client=client,
        time=datetime.now()
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data



def read_reading_Ids(db: Session):
    return db.query(models.id).filter(models.id == id).first()

def read_reading_Celsius(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Readings.temp_c).offset(skip).limit(limit).all()

def read_reading_Fahrenheit(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Readings.temp_f).offset(skip).limit(limit).all()

def update_reading(db: Session, id: int): #Responsible for Celsius
    db.query(models.Readings.temp_c).where(models.Readings.id == id).\
        update(("temp_c": temp_c, "temp_f": temp_f), synchronize_session="evaluate")

    db.commit()

    return db.query(models.Readings).where(models.Readings.id == id).first()

def delete_reading(db: Session, id: int):
    db.query(models.Readings).filter(models.Readings.id == id).\
        delete(synchronize_session=False)

    db.commit()

    return {"msg": f"Temperature with ID:{id} deleted"}

def create_reading(db: Session, id: int, temp: float, client: str, is_celsius: bool) -> None:
    if is_celsius:
        temp_c = temp
        temp_f = (temp * 9/5) + 32
    else:
        temp_f = temp
        temp_c = (temp - 32) * 5/9
        
    create_reading(db, id, temp_c, temp_f, client)

def read_reading(db: Session) -> list:
    return db.query(models.Readings).all()

def read_reading_by_id(db: Session, id: int) -> list:
    return db.query(models.Readings).filter_by(id=id).all()

def read_reading_temperature(db: Session, id: int, is_celsius: bool) -> float:
    reading = db.query(models.Readings).filter_by(id=id).first()
    if reading:
        return reading.temp_celsius if is_celsius else reading.temp_fahrenheit
    return None

def read_reading_by_client_and_time(db: Session, client: str, time: datetime) -> list:
    return db.query(models.Readings).filter_by(person=client).filter(models.Readings.timestamp <= time).all()
