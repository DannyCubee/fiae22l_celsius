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


def delete_reading():
    pass


