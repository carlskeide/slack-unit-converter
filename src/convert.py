# coding=utf-8
import logging
from datetime import date

from flack.message import PrivateResponse

from pint import UnitRegistry
from pint.errors import UndefinedUnitError

from . import redis

logger = logging.getLogger(__name__)

UNIT_KEY = "TZ:UNITS"


def _load_units():
    units = UnitRegistry()

    custom_units = redis.hgetall(UNIT_KEY)
    logger.info("Loading units (%d custom definitions)", len(custom_units))

    for name, definition in custom_units.items():
        logger.debug("loading custom unit: %s = %s", name, definition)

        if definition.startswith("__age"):
            birthday = date.fromisoformat(definition.split(" ")[1])
            age = (date.today() - birthday).total_seconds()

            definition = f"{age} seconds"
            logger.debug("Converted date: %s to: %s", birthday, definition)

        units.define(f"{name} = {definition}")

    return units


def register_unit(name, conversion):
    logger.info("Registering unit: %s = %s", name, conversion)

    if not name.isalpha():
        return PrivateResponse("Custom units can only contain letters")

    if conversion.startswith("birthday "):
        try:
            raw_date = conversion.split(" ")[1].strip()
            birthday = date.fromisoformat(raw_date)

        except Exception:
            logger.exception("Unable to parse birthday: %s", conversion)
            return PrivateResponse("birthdays must be iso-formatted")

        # Converted to seconds from now in _load_units()
        definition = f"__age {birthday}"

    else:
        # Custom units must map to standard units
        try:
            units = UnitRegistry()
            to_unit = units(conversion)

        except UndefinedUnitError:
            return PrivateResponse(f"Unknown conversion unit: {conversion}")

        definition = f"{to_unit.m} {to_unit.u}"

    try:
        redis.hset(UNIT_KEY, name, definition)

    except Exception:
        logger.exception("Unable to register unit: %s = %s", name, definition)
        return PrivateResponse("Internal error")

    return f"New unit defined: {name}"


def unregister_unit(name):
    logger.info("Unregistering unit: %s", name)

    try:
        definition = redis.hget(UNIT_KEY, name)
        if not definition:
            return PrivateResponse(f"Custom unit {name} is not defined")

        redis.hdel(UNIT_KEY, name)

        logger.warning("Removed custom unit: %s = %s", name, definition)
        return f"Removed custom unit: {name}"

    except Exception:
        logger.exception("Unable to unregister unit: %s", name)
        return PrivateResponse("Internal error")


def unit_converter(src, dest):
    logger.info("Converting %s to %s", src, dest)

    try:
        units = _load_units()

    except Exception:
        logger.exception("Unable to load units")
        return PrivateResponse("Internal error")

    try:
        src_unit = units(src)
        result = src_unit.to(units(dest))
    except Exception as e:
        logger.warning("Conversion failed: %r", e)
        return PrivateResponse(f"Conversion failed: {e}")

    logger.debug("Conversion result: %s", result)

    neat_result = f"{result.m:.02f}".rstrip('0').rstrip('.')
    return f"{src_unit!s} =~ {neat_result} {result.u}"
