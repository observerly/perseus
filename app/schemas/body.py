from pydantic import BaseModel


# Shared properties
class BodyBase(BaseModel):
    # Unique ID:
    uid: str
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
    m: float
    # Absolute Magnitude:
    M: float
    # distance
    d: float
    # HD Number:
    hd: str | None = None
    # HR Number:
    hr: str | None = None
    # Hipparcos Number
    hip: str | None = None
    # BD Number:
    bd: str | None = None
    # Flamsteed Number:
    flamsteed: str | None = None
    # Messier Number:
    messier: str | None = None
    # NGC Number:
    ngc: str | None = None
    # IC Number:
    ic: str | None = None


# Properties shared by models stored in DB
class BodyInDBBase(BodyBase):
    class Config:
        orm_mode = True


# Properties to return to client
class Body(BodyInDBBase):
    pass


# Properties properties stored in DB
class BodyInDB(BodyInDBBase):
    pass
