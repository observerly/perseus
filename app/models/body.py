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

    # The IAU Authoritative/Designated Name
    iau = Column(
        String(
            length=180,
            collation="utf8",
            convert_unicode=False,
            unicode_error=None,
        ),
        index=True,
        name="iau",
        comment="IAU Name",
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
        index=False,
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
        index=False,
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
        index=False,
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
        index=False,
        name="absolute_magnitude",
        comment="Absolute Magnitude (M)",
    )

    # Distance to the star (in parsecs).
    d = Column(
        Float(
            precision=5,
            asdecimal=True,
            decimal_return_scale=10,
        ),
        index=False,
        name="distance",
        comment="Distance (in parsecs, pc)",
    )

    # Henry Draper Catalogue Number:
    # The HD catalogue is named after Henry Draper, an amateur astronomer, and
    # covers the entire sky almost completely down to an apparent photographic
    # magnitude of about 9; the extensions added fainter stars in certain areas
    # of the sky.
    hd = Column(
        String(
            length=180,
            collation="utf8",
            convert_unicode=False,
            unicode_error=None,
        ),
        index=True,
        name="hd",
        comment="Henry Draper (HD) Catalogue Number",
    )

    # Harvard Revised Catalogue Number
    hr = Column(
        String(
            length=180,
            collation="utf8",
            convert_unicode=False,
            unicode_error=None,
        ),
        index=True,
        name="hr",
        comment="Harvard Revised (HR) Catalogue Number",
    )

    # Hipparcos Catalogue Number
    hip = Column(
        String(
            length=180,
            collation="utf8",
            convert_unicode=False,
            unicode_error=None,
        ),
        index=True,
        name="hip",
        comment="Hipparcos (HIP) Catalogue Number",
    )

    # Durchmusterung Catalogue Number:
    # Durchmusterung or Bonner Durchmusterung (BD), is an astrometric star
    # catalogue of the whole sky, compiled by the Bonn Observatory in
    # Germany from 1859 to 1903.
    bd = Column(
        String(
            length=180,
            collation="utf8",
            convert_unicode=False,
            unicode_error=None,
        ),
        index=True,
        name="bd",
        comment="Hipparcos (HIP) Catalogue Number",
    )

    # A Flamsteed designation is a combination of a number and constellation
    # name that uniquely identifies most naked eye stars in the modern
    # constellations visible from southern England. They are named for
    # John Flamsteed who first used them while compiling his Historia
    # Coelestis Britannica. (Flamsteed used a telescope,[1] and the catalog
    #  also includes some stars which are relatively bright but not
    # necessarily visible with the naked eye.)
    flamsteed = Column(
        String(
            length=10,
            collation="utf8",
            convert_unicode=False,
            unicode_error=None,
        ),
        index=True,
        name="flamsteed",
        comment="Flamsteed Catalogue Number",
    )

    # Messier Catalogue Number:
    # The Messier objects are a set of 110 astronomical objects catalogued by
    # the French astronomer Charles Messier in his Catalogue des Nébuleuses et
    # des Amas d'Étoiles (Catalogue of Nebulae and Star Clusters). Because
    # Messier was only interested in finding comets, he created a list of those
    # non-comet objects that frustrated his hunt for them.
    messier = Column(
        String(
            length=3,
            collation="utf8",
            convert_unicode=False,
            unicode_error=None,
        ),
        index=True,
        name="messier",
        comment="Messier Catalogue Number",
    )

    # NGC Catalogue Number:
    # The New General Catalogue of Nebulae and Clusters of Stars (abbreviated NGC)
    #  is an astronomical catalogue of deep-sky objects compiled by John Louis
    # Emil Dreyer in 1888. The NGC contains 7,840 objects, including galaxies,
    # star clusters and emission nebulae.
    ngc = Column(
        String(
            length=3,
            collation="utf8",
            convert_unicode=False,
            unicode_error=None,
        ),
        index=True,
        name="ngc",
        comment="New General Catalogue (NGC) Number",
    )

    # Indexed Catalogues Number:
    # Dreyer published two supplements to the NGC in 1895 and 1908, known as the
    # Index Catalogues (abbreviated IC), describing a further 5,386 astronomical
    # objects. Thousands of these objects are best known by their NGC or IC numbers,
    # which remain in widespread use.
    ic = Column(
        String(
            length=3,
            collation="utf8",
            convert_unicode=False,
            unicode_error=None,
        ),
        index=True,
        name="ic",
        comment="Indexed Catalogue (IC) Number",
    )

    #  SIMBAD Search Query URL
    simbad = Column(
        String(
            length=200,
            collation="utf8",
            convert_unicode=False,
            unicode_error=None,
        ),
        index=False,
        name="simbad",
        comment="SIMBAD Search Query URL",
    )


@event.listens_for(Body, "before_update")
def receive_before_update(mapper, conenction, target):
    target.constellation = SkyCoord(
        ra=target.ra * u.degree,
        dec=target.dec * u.degree,
        frame=FRAME,
    ).get_constellation()
