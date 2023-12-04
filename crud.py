# CRUD Anweisungen für unsere Datenbankabfragen

from sqlalchemy.orm import Session, Query

from . import models, schemas


def create_reading(db: Session, id: int, temp_c: float, temp_f: float, client: str):
    new_data = models.Readings(id=id, temp_c=temp_c, temp_f=temp_f, client=client)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data


def read_reading(db: Session):
    pass


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


