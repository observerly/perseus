from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


# Shared properties from Perseus API:
class BodyBase(BaseModel):
    """
    Base model for all astronomical objects, inc. stars, galaxies and nebulae.
    """

    # Unique ID:
    uid: UUID = Field(
        default_factory=uuid4,
        title="Unique ID",
        description="Unique ID for the astronomical object.",
    )
    # Common Name:
    name: str = Field(
        "",
        title="Common Name",
        description="The common name of the astronomical object as defined by \
            astronomical community standards, e.g., M31 would have a common \
            name of the Andromeda Galaxy",
    )
    # IAU Name:
    iau: str = Field(
        "",
        title="International Astronomical Union Name",
        description="The common name of the astronomical object as defined by \
            International Astronomical Union, e.g., the Andromeda Galaxy would \
            have an IAU name of M31",
    )
    # Right Ascension
    ra: Optional[float] = Field(
        None,
        title="Right Ascension",
        description="The right ascension, α, of the astronomical object in degrees",
    )
    # Declination
    dec: Optional[float] = Field(
        None,
        title="Declination",
        description="The declination, δ, of the astronomical object in degrees",
    )
    # Constellation
    constellation: str = Field(
        "",
        title="Constellation",
        description="The constellation in which the astronomical object is located",
    )
    # Object Type
    type: str = Field(
        "S",
        title="Object Type",
        description="The type of astronomical object, please see the documentation \
            for a list of types",
    )
    # Apparent Magnitude:
    m: Optional[float] = Field(
        None,
        title="Apparent Magnitude, m",
        description="The apparent magnitude of the astronomical object",
    )
    # Absolute Magnitude:
    M: Optional[float] = Field(
        None,
        title="Absolute Magnitude, M",
        description="The absolute magnitude of the astronomical object",
    )
    # distance
    d: Optional[float] = Field(
        None,
        title="Distance",
        description="The distance to the astronomical object in parsecs",
    )
    # HD Number:
    hd: Optional[str] = Field(
        None,
        title="HD Number",
        description="The Henry Draper catalgoue number",
    )
    # HR Number:
    hr: Optional[str] = Field(
        None,
        title="HR Number",
        description="The Harvard Revised number",
    )
    # Hipparcos Number
    hip: Optional[str] = Field(
        None,
        title="Hipparcos Number",
        description="The Hipparcos Survey catalogue number",
    )
    # BD Number:
    bd: Optional[str] = Field(
        None,
        title="BD Number",
        description="The Bonner-Durchmusterung catalogue number",
    )
    # Flamsteed Number:
    flamsteed: Optional[str] = Field(
        None,
        title="Flamsteed Number",
        description="The Flamsteed catalogue number",
    )
    # Messier Number:
    messier: Optional[str] = Field(
        None,
        title="Messier Number",
        description="The Messier catalogue number",
    )
    # NGC Number:
    ngc: Optional[str] = Field(
        None,
        title="NGC Number",
        description="The New General Catalogue number",
    )
    # IC Number:
    ic: Optional[str] = Field(
        None,
        title="IC Number",
        description="The Index Catalogue number",
    )
    # Eccentricity:
    e: Optional[float] = Field(
        None,
        title="Eccentricity",
        description="The eccentricity of the astronomical object (unitless)",
    )
    # Semi-major Axis:
    a: Optional[float] = Field(
        None,
        title="Semi-major Axis",
        description="The semi-major axis of the astronomical object in arcminutes",
    )
    # Semi-minor Axis:
    b: Optional[float] = Field(
        None,
        title="Semi-minor Axis",
        description="The semi-minor axis of the astronomical object in arcminutes",
    )
    # Inclination:
    i: Optional[float] = Field(
        None,
        title="Inclination",
        description="The inclination relative to the ecliptic \
            of the astronomical object in degrees",
    )
    # Redshift
    z: Optional[float] = Field(
        None,
        title="Redshift",
        description="The redshift of the astronomical object",
    )
    # SIMBAD Query URL:
    simbad: Optional[str] = Field(
        None,
        title="SIMBAD Query URL",
        description="The SIMBAD Query URL of the astronomical object",
    )

    class Config:
        title = "Body"


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
    # Eccentricity:
    e: Optional[float] = None
    # Semi-major Axis:
    a: Optional[float] = None
    # Semi-minor Axis:
    b: Optional[float] = None
    # Inclination:
    i: Optional[float] = None
    # Redshift
    z: Optional[float] = None
    # SIMBAD
    simbad: Optional[str] = None


class BodyUpdate(BodyBase):
    pass
