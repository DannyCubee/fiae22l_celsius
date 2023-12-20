# CRUD Anweisungen für unsere Datenbankabfragen
from sqlalchemy.orm import Session
from sqlalchemy import update
from typing import Optional
from datetime import datetime
from sqlalchemy import desc

from . import models


def create_reading(db: Session, temp_c: float, temp_f: float, client: str):
    new_data = models.Readings(
        temp_c=temp_c,
        temp_f=temp_f,
        client=client,
        time=datetime.now()

    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)

def filter_reading(
        db: Session,
        id: Optional[int] = None,
        client: Optional[str] = None,
        einheit: Optional[str] = None,
        von: Optional[datetime] = None,
        bis: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
) -> list:
    query = db.query(models.Readings)
    if id is not None:
        query = query.filter(models.Readings.id == id)
    if client is not None:
        query = query.filter(models.Readings.client == client)
    if einheit is not None:
        if einheit.equals("celsius"):
            query = query.with_entities(models.Readings.temp_c)
        elif einheit.equals("fahrenheit"):
            query = query.with_entities(models.Readings.temp_f)
    if von is not None:
        query = query.filter(models.Readings.time >= von)
    if bis is not None:
        query = query.filter(models.Readings.time <= bis)
    return query.offset(skip).limit(limit).all()


def read_all(db: Session, skip: int = 0, limit: int = 100) -> list[models.Readings]:
    return db.query(models.Readings).offset(skip).limit(limit).all()


def read_by_id(db: Session, id: int):
    return db.query(models.Readings).filter(models.Readings.id==id).first()


def read_Temperature(db: Session, id: int, einheit: str, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, id=id, einheit=einheit, skip=skip, limit=limit)


def read_Celsius(db: Session, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, einheit="celsius", skip=skip, limit=limit)


def read_Fahrenheit(db: Session, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, einheit="fahrenheit", skip=skip, limit=limit)


def read_by_Client(db: Session, client: str, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, client=client, skip=skip, limit=limit)


def read_by_Time(db: Session, time: datetime, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, von=time, bis=time, skip=skip, limit=limit)


def read_by_Timeframe(db: Session, von: datetime, bis: datetime, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, von=von, bis=bis, skip=skip, limit=limit)


def read_by_Client_and_Time(db: Session, client: str, time: datetime, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, client=client, time=time, skip=skip, limit=limit)


def update_reading(
        db: Session,
        id: int,
        temp_c: Optional[float] = None,
        temp_f: Optional[float] = None,
        client: Optional[str] = None,
        time: Optional[datetime] = None,
) -> None:
    update_values = {}
    if temp_c is not None:
        update_values['temp_c'] = temp_c
    if temp_f is not None:
        update_values['temp_f'] = temp_f
    if client is not None:
        update_values['client'] = client
    if time is not None:
        update_values['time'] = time

    db.execute(
        update(models.Readings).
        where(models.Readings.id == id).
        values(**update_values)
    )
    db.commit()


def update_Time(db: Session, id: int, skip: int = 0, limit: int = 100) -> None:
    time_input = input("Bitte gebe eine neue Zeit ein: ")
    update_reading(db=db, id=id, time=time_input)


def delete_all(db: Session) -> None:
    db.query(models.Readings).delete()
    db.commit()


def delete_by_Id(db: Session, id: int):
    entries = read_by_Id(db, id=id)
    if entries:
        for entry in entries:
            db.delete(entry)
        db.commit()
    return {"msg": f"Temperature with ID:{id} deleted"}


def delete_by_Client(db: Session, cliemt: str, skip: int = 0, limit: int = 100) -> None:
    entries_to_delete = read_by_Client(db=db, client=cliemt, skip=skip, int=int, limit=limit)

    for entry in entries_to_delete:
        delete_by_Id(db, entry.id)


def delete_by_Time(db: Session, time: datetime, skip: int = 0, limit: int = 100) -> None:
    entries_to_delete = read_by_Time(db=db, time=time, skip=skip, int=int, limit=limit)

    for entry in entries_to_delete:
        delete_by_Id(db, entry.id)


def delete_by_timeframe(db: Session, client: str, von: datetime, bis: datetime, skip: int = 0,
                        limit: int = 100) -> None:
    entries_to_delete = read_by_Timeframe(db, client=client, von=von, bis=bis, skip=skip, limit=limit)
    for entry in entries_to_delete:
        delete_by_Id(db, entry.id)


def delete_by_client_and_time(db: Session, client: str, time: datetime, skip: int = 0, limit: int = 100) -> None:
    entries_to_delete = read_by_Client_and_Time(db, client=client, time=time, skip=skip, limit=limit)
    for entry in entries_to_delete:
        delete_by_Id(db, entry.id)

    return new_data


def get_all_readings(db: Session) -> list:
    return db.query(models.Readings).all()


def read_reading_by_id(db: Session) -> list:
    return db.query(models.Readings).filter_by(id=id).all()


def get_last_reading(db: Session):
    return db.query(models.Readings).order_by(desc(models.Readings.id)).first()


def read_reading_Temperature(db: Session, id: int, is_celsius: bool) -> float:
    reading = db.query(models.Readings).filter_by(id=id).first()
    if reading:
        return reading.temp_c if is_celsius else reading.temp_f
    return None


def read_reading_Celsius(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Readings.temp_c).offset(skip).limit(limit).all()


def read_reading_fahrenheit(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Readings.temp_f).offset(skip).limit(limit).all()


def read_reading_by_client(db: Session, client: str) -> list:
    return db.query(models.Readings).filter(models.Readings.client==client).all()


def read_reading_by_Client_and_Time(db: Session, client: str, time: datetime) -> list:
    return db.query(models.Readings).filter(models.Readings.time <= time, models.Readings.client == client).all()


def delete_reading(db: Session, id: int):
    db.query(models.Readings).filter(models.Readings.id == id). \
        delete(synchronize_session=False)
    db.commit()
    return {"msg": f"Temperature with ID:{id} deleted"}


def get_reading_by_timeframe(db: Session, start: datetime, end: datetime):
    data = db.query(models.Readings).filter(models.Readings.time >= start, models.Readings.time <= end).all()
    return data
