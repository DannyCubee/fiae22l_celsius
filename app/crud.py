# CRUD Anweisungen für unsere Datenbankabfragen

#Imports
from sqlalchemy.orm import Session
from sqlalchemy import update
from typing import Optional
from datetime import datetime
from sqlalchemy import desc
from . import models

#Anlegen eines Neuen Datensatz mit allen gegebenen Daten der in die Datenbank eingefügt wird
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

#Funktion zum Filtern zurückgegebener Datenbankeinträge
def filter_reading(
        db: Session,
        id: Optional[int] = None,
        client: Optional[str] = None,
        einheit: Optional[str] = None,
        von: Optional[datetime] = None,
        bis: Optional[datetime] = None,
        skip: int = 0,
        limit: int = None
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

#Liest alle Einträge einer Datenbank aus
def get_all_readings(db: Session, skip: int = 0, limit: int = 100) -> list[models.Readings]:
    return db.query(models.Readings).offset(skip).limit(limit).all()

#Liest alle Einträge zu der übergebenen ID
def read_by_id(db: Session, id: int):
    return db.query(models.Readings).filter(models.Readings.id==id).first()

#Liest Ids aus, in aufsteigender oder abfallender Reihenfolge
def read_ids(db: Session, desc: bool = False, skip: int = 0, limit: int = 100) -> list:
    if desc:
        # Sortiere IDs in abfallender Reihenfolge
        return db.query(models.Readings.id).order_by(models.Readings.id.desc()).offset(skip).limit(limit).all()
    else:
        # Sortiere IDs in aufsteigender Reihenfolge
        return db.query(models.Readings.id).order_by(models.Readings.id.asc()).offset(skip).limit(limit).all()

#Gibt den eintrag zmit der zuletzt eingefügten ID zurück
def get_last_reading(db: Session):
    return read_by_id(read_ids(db, True, limit=1))

#Gibt Temperaturdatensätze zu einer ID zurück.
def read_reading_temperature(db: Session, id: int, is_celsius: bool, skip: int = 0, limit: int = 100) -> list:
    if is_celsius:
        return filter_reading(db, id=id, einheit="celsius", skip=skip, limit=limit)
    else:
        return filter_reading(db, id=id, einheit="fahrenheit", skip=skip, limit=limit)

#Gibt Celsius-Temperaturwerte zurück
def read_reading_celsius(db: Session, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, einheit="celsius", skip=skip, limit=limit)

#Gibt Fahrenheit-Temperaturwerte zurück
def read_reading_fahrenheit(db: Session, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, einheit="fahrenheit", skip=skip, limit=limit)

#Gibt Datensätze eines Client zurück
def read_reading_by_client(db: Session, client: str, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, client=client, skip=skip, limit=limit)

#Gibt Datensätze zu einem spezifischen Zeitpunkt zurück.
def read_reading_by_time(db: Session, time: datetime, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, von=time, bis=time, skip=skip, limit=limit)

#Gibt Datensätze in auf einem spezifischen Zeitraum zurück.
def get_reading_by_timeframe(db: Session, von: datetime, bis: datetime, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, von=von, bis=bis, skip=skip, limit=limit)

#Gibt Datensätze zurück, die sowohl einem Client als auch einem Zeitpunkt oder Zeitraum entsprechen.
def read_reading_by_client_and_time(db: Session, client: str, time: datetime, skip: int = 0, limit: int = 100) -> list:
    return filter_reading(db, client=client, time=time, skip=skip, limit=limit)

#Aktualisiert einen Datensatz basierend auf seiner ID und optionalen Parametern wie Temperatur, Client und Zeit.
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


#Aktualisiert die Zeit in einem Eintrag des Datensatzes
def update_Time(db: Session, id: int, skip: int = 0, limit: int = 100) -> None:
    time_input = input("Bitte gebe eine neue Zeit ein: ")
    update_reading(db=db, id=id, time=time_input)

#Löscht alle Datensätze in der Datenbank
def delete_all(db: Session) -> None:
    db.query(models.Readings).delete()
    db.commit()

#Löscht Datensätze basierend auf ihrer ID
def delete_reading(db: Session, id: int):
    entries = read_by_id(db, id=id)
    if entries:
        for entry in entries:
            db.delete(entry)
        db.commit()
    return {"msg": f"Temperature with ID:{id} deleted"}

#Löscht Datensätze basierend auf ihrer ID
def delete_by_client(db: Session, cliemt: str, skip: int = 0, limit: int = 100) -> None:
    entries_to_delete = read_reading_by_client(db=db, client=cliemt, skip=skip, int=int, limit=limit)
    for entry in entries_to_delete:
        delete_reading(db, entry.id)

#Löscht Datensätze eines Client
def delete_by_Time(db: Session, time: datetime, skip: int = 0, limit: int = 100) -> None:
    entries_to_delete = read_reading_by_time(db=db, time=time, skip=skip, int=int, limit=limit)
    for entry in entries_to_delete:
        delete_reading(db, entry.id)

#Löscht Datensätze zu einem übergebene Zeitpunkt
def delete_by_timeframe(db: Session, client: str, von: datetime, bis: datetime, skip: int = 0, limit: int = 100) -> None:
    entries_to_delete = get_reading_by_timeframe(db, client=client, von=von, bis=bis, skip=skip, limit=limit)
    for entry in entries_to_delete:
        delete_reading(db, entry.id)

#Löscht Datensätze eines bestimmten Clients zu einem gewissen Zeitpunkts
def delete_by_client_and_time(db: Session, client: str, time: datetime, skip: int = 0, limit: int = 100) -> None:
    entries_to_delete = read_reading_by_client_and_time(db, client=client, time=time, skip=skip, limit=limit)
    for entry in entries_to_delete:
        delete_reading(db, entry.id)