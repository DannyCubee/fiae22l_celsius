from pydantic import BaseModel


class Temperature(BaseModel):
    temp_c: float
    temp_f: float



