from pydantic import BaseModel
from datetime import datetime


class Temperature(BaseModel):
    time: datetime
    temp_c: float
    temp_f: float
    client: str


class TemperatureCelsius(BaseModel):
    time: datetime
    temp_c: float
    client: str


class TemperatureFahrenheit(BaseModel):
    time: datetime
    temp_f: float
    client: str






