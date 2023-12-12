# Definition der Datenbankmodelle. Tabellen können hier direkt erstellt werden und müssen nicht in der SQLite Anwendung
# erstellt werden

from sqlalchemy import Column, Integer, Float, String, DateTime

from database import Base


class Readings(Base):
    __tablename__ = "Readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    temp_c = Column(Float)
    temp_f = Column(Float)
    client = Column(String)
    time   = Column(DateTime)
