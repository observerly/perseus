from astropy import units as u
from astropy.coordinates import SkyCoord
from sqlalchemy import Column, Float, String, event
from sqlalchemy import text as sa_text
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

FRAME = "icrs"


class Body(Base):
    # UID as primary key
    uid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sa_text("uuid_generate_v4()"),
    )

    # Common Name
    name = Column(
        String(
            length=180,
            collation="utf8",
            convert_unicode=False,
            unicode_error=None,
        ),
        index=True,
        name="name",
        comment="Common or IAU Name",
    )

    # Right ascension (abbreviated RA; symbol α) is the angular distance of a
    # particular point measured eastward along the celestial equator from the
    # Sun at the March equinox to the (hour circle of the) point in question
    # above the earth.
    ra = Column(
        Float(
            precision=10,
            asdecimal=True,
            decimal_return_scale=10,
        ),
        index=True,
        name="ra",
        comment="Right Ascension of the central point of the Body",
    )

    # Declination (abbreviated dec; symbol δ) is one of the two angles that
    # locate a point on the celestial sphere in the equatorial coordinate system,
    # the other being hour angle. Declination's angle is measured north or south
    # of the celestial equator, along the hour circle passing through the point
    # in question
    dec = Column(
        Float(
            precision=10,
            asdecimal=True,
            decimal_return_scale=10,
        ),
        name="dec",
        index=True,
        comment="Declination of the central point of the Body",
    )

    # Constellation (Contained Within)
    constellation = Column(
        String(
            length=180,
            collation="utf8",
            convert_unicode=False,
            unicode_error=None,
        ),
        index=True,
        name="constellation",
        comment="IAU Constellation (Contained Within)",
    )

    # Body Object Type
    type = Column(
        String(
            length=180,
            collation="utf8",
            convert_unicode=False,
            unicode_error=None,
        ),
        index=True,
        name="type",
        comment="Celestial Body Type e.g., Star, Spiral Galaxy etc",
    )

    # Apparent magnitude (m) is a measure of the brightness of an astronomical
    # object observed from Earth. An object's apparent magnitude depends on its
    # intrinsic luminosity, its distance from Earth, and any extinction of the
    # object's light caused by interstellar dust along the line of sight to
    # the observer.
    m = Column(
        Float(
            precision=5,
            asdecimal=True,
            decimal_return_scale=10,
        ),
        index=True,
        name="apparent_magnitude",
        comment="Apparent Magnitude (m)",
    )

    # Absolute magnitude (M) is a measure of the luminosity of a celestial
    # object, on an inverse logarithmic astronomical magnitude scale. An
    # object's absolute magnitude is defined to be equal to the apparent
    # magnitude that the object would have if it were viewed from a distance
    # of exactly 10 parsecs (32.6 light-years), without extinction (or
    # dimming) of its light due to absorption by interstellar matter and
    # cosmic dust.
    M = Column(
        Float(
            precision=5,
            asdecimal=True,
            decimal_return_scale=10,
        ),
        index=True,
        name="apparent_magnitude",
        comment="Absolute Magnitude (M)",
    )


@event.listens_for(Body, "before_update")
def receive_before_update(mapper, conenction, target):
    target.constellation = SkyCoord(
        ra=target.ra * u.degree,
        dec=target.dec * u.degree,
        frame=FRAME,
    ).get_constellation()
