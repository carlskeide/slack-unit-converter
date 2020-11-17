# coding=utf-8
import logging
from argparse import ArgumentParser

from flask import Flask
from flask_redis import FlaskRedis
from flack import Flack
from flack.message import PrivateResponse

from . import config

logging.basicConfig(level=config.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(config)

flack = Flack(app)

redis = FlaskRedis(app, decode_responses=True)

# Avoids circular dependency by importing after app/redis are defined
from . import convert  # noqa


class InlineArgumentParser(ArgumentParser):
    def error(self, message):
        raise Exception(message + "\n" + self.format_usage())


@flack.command("/convert")
def command_convert(text, **kwargs):
    parser = InlineArgumentParser(
        prog="/convert", add_help=False)
    parser.add_argument(
        "args", type=str, nargs="+",
        help="*qty* *unit* to *unit*")

    try:
        parsed = parser.parse_args(text.split())
        args = " ".join(parsed.args)
        src, dest = args.split(' to ')

    except Exception:
        return PrivateResponse(parser.format_usage())

    else:
        return convert.unit_converter(src, dest)


@flack.command("/define")
def command_define(text, **kwargs):
    parser = InlineArgumentParser(
        prog="/define", add_help=False)
    parser.add_argument(
        "-u", action="store_true", dest="undefine",
        help="Undefine a custom unit")
    parser.add_argument(
        "definition", type=str, nargs="+",
        help="Definition")

    try:
        parsed = parser.parse_args(text.split())
        args = " ".join(parsed.definition)

    except Exception:
        return PrivateResponse(parser.format_usage())

    if parsed.undefine:
        return convert.unregister_unit(args)

    try:
        name, conversion = args.split(" = ")
        return convert.register_unit(name, conversion)

    except Exception:
        return PrivateResponse("Usage: `/define *new_unit* = *qty* *unit*`")
