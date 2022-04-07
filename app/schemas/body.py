from typing import Optional
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class BodyBase(BaseModel):
    # Unique ID:
    uid: UUID
    # Common Name:
    name: str
    # IAU Name:
    iau: str
    # Right Ascension
    ra: Optional[float] = None
    # Declination
    dec: Optional[float] = None
    # Constellation
    constellation: str
    # Object Type
    type: str
    # Apparent Magnitude:
    m: Optional[float] = None
    # Absolute Magnitude:
    M: Optional[float] = None
    # distance
    d: Optional[float] = None
    # HD Number:
    hd: Optional[str] = None
    # HR Number:
    hr: Optional[str] = None
    # Hipparcos Number
    hip: Optional[str] = None
    # BD Number:
    bd: Optional[str] = None
    # Flamsteed Number:
    flamsteed: Optional[str] = None
    # Messier Number:
    messier: Optional[str] = None
    # NGC Number:
    ngc: Optional[str] = None
    # IC Number:
    ic: Optional[str] = None
    # SIMBAD
    simbad: Optional[str] = None


# Properties shared by models stored in DB
class BodyInDBBase(BodyBase):
    # Unique ID:
    uid: UUID

    class Config:
        orm_mode = True


# Properties to return to client
class Body(BodyInDBBase):
    pass


# Properties properties stored in DB
class BodyInDB(BodyInDBBase):
    pass


class BodyCreate(BaseModel):
    # Common Name:
    name: str
    # IAU Name:
    iau: str
    # Right Ascension
    ra: float
    # Declination
    dec: float
    # Constellation
    constellation: str
    # Object Type
    type: str
    # Apparent Magnitude:
    m: Optional[float] = None
    # Absolute Magnitude:
    M: Optional[float] = None
    # distance
    d: Optional[float] = None
    # HD Number:
    hd: Optional[str] = None
    # HR Number:
    hr: Optional[str] = None
    # Hipparcos Number
    hip: Optional[str] = None
    # BD Number:
    bd: Optional[str] = None
    # Flamsteed Number:
    flamsteed: Optional[str] = None
    # Messier Number:
    messier: Optional[str] = None
    # NGC Number:
    ngc: Optional[str] = None
    # IC Number:
    ic: Optional[str] = None
    # SIMBAD
    simbad: Optional[str] = None


class BodyUpdate(BodyBase):
    pass
