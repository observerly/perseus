import json
from logging import Logger

from sqlalchemy.orm import Session

from app import crud, schemas
from app.utils import ROOT_DIR


def seed_stars(db: Session, logger: Logger) -> None:
    """
    This function call seeds the Body model with a known set of stars in data directory
    """
    count = 0

    logger.info("ROOT_DIR: {}".format(ROOT_DIR))

    data = None

    stars = []

    # Open the majorStars.json file:
    with open("{}/data/stars/majorStars.json".format(ROOT_DIR), "r") as f:
        data = json.loads(f.read())

    # Read the stars
    for star in data:
        s = {
            "name": star["bayer"],
            "iau": star["iau"],
            "ra": float(star["ra"]),
            "dec": float(star["dec"]),
            "constellation": star["constellation"],
            "type": "*",
            "hd": star["hd"],
            "hr": star["hr"],
            "hip": star["hip"],
            "bd": star["dm"],
            "flamsteed": star["flamsteed"],
            "simbad": star["query"],
        }

        s["m"] = (
            lambda star: None
            if star["apparentMagnitude"] is None
            else float(star["apparentMagnitude"])
        )(star)

        s["M"] = (
            lambda star: None
            if star["absoluteMagnitude"] is None
            else float(star["absoluteMagnitude"])
        )(star)

        s["d"] = (lambda star: None if star["d"] is None else float(star["d"]))(star)

        star_in = schemas.BodyCreate(**s)
        stars.append(star_in)

    for star_in in stars:
        crud.body.create(db, body=star_in)  # noqa: F841
        count += 1
        logger.info("Successfully Populated Star {}".format(star_in.name))

    # Read the stars incrementally into the db:

    logger.info("Populated Initial API w/{} Stars".format(count))


def seed_galaxies(db: Session, logger: Logger) -> None:
    pass


def seed_nebulae(db: Session, logger: Logger) -> None:
    pass
