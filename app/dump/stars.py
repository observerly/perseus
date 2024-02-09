import json
from logging import Logger

from sqlalchemy.orm import Session

from app.utils import ROOT_DIR


def dump_stars(db: Session, logger: Logger) -> None:
    """
    This function call dumps the Body model with a known set of stars in data directory
    """
    count = 0

    logger.info("ROOT_DIR: {}".format(ROOT_DIR))

    data = None

    stars = []

    data = []

    # Open the majorStars.json file:
    with open("{}/data/stars/majorStars.json".format(ROOT_DIR), "r") as f:
        data += json.loads(f.read())

    with open("{}/data/stars/minorStars.json".format(ROOT_DIR), "r") as f:
        data += json.loads(f.read())

    with open("{}/data/stars/peripheralStars.json".format(ROOT_DIR), "r") as f:
        data += json.loads(f.read())

    # Read the stars
    for star in data:
        s = {
            "name": star["bayer"],
            "iau": star["iau"],
            "ra": star["ra"],
            "dec": star["dec"],
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
            else star["apparentMagnitude"]
        )(star)

        s["M"] = (
            lambda star: None
            if star["absoluteMagnitude"] is None
            else star["absoluteMagnitude"]
        )(star)

        s["d"] = (lambda star: None if star["d"] is None else star["d"])(star)

        stars.append(s)

        count += 1

    print(stars)

    # Dump the stars to a json file:
    with open("{}/data/stars/stars.json".format(ROOT_DIR), "w") as f:
        f.write(json.dumps(stars))

    # Read the stars incrementally into the db:
    logger.info("Dumped Initial API w/{} Stars".format(count))
