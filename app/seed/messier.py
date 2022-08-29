import json
from logging import Logger

from sqlalchemy.orm import Session

from app import crud, schemas
from app.utils import ROOT_DIR


def seed_messier(db: Session, logger: Logger) -> None:
    """
    This function call seeds the Body model with a known set of Messier
    objects in data directory
    """
    count = 0

    logger.info("ROOT_DIR: {}".format(ROOT_DIR))

    objects = []

    data = []

    # Open the majorStars.json file:
    with open("{}/data/objects/messier.json".format(ROOT_DIR), "r") as f:
        data += json.loads(f.read())

    for body in data:
        m = {
            "name": body["name"],
            "iau": body["iau"],
            "ra": float(body["ra"]),
            "dec": float(body["dec"]),
            "constellation": body["constellation"],
            "type": body["type"],
            "messier": body["messier"],
            "ngc": body["ngc"],
            "ic": body["ic"],
            "simbad": body["simbad"],
        }

        m["m"] = (lambda body: None if body["m"] is None else float(body["m"]))(body)

        m["M"] = (lambda body: None if body["M"] is None else float(body["M"]))(body)

        m["d"] = (lambda body: None if body["d"] is None else float(body["d"]))(body)

        object_in = schemas.BodyCreate(**m)
        objects.append(object_in)

    for object_in in objects:
        crud.body.create(db, body=object_in)  # noqa: F841
        count += 1
        logger.info("Successfully Populated Object {}".format(object_in.name))

    # Read the stars incrementally into the db:

    logger.info("Populated Initial API w/{} Objects".format(count))
