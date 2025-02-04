#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AIM backend server.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, Tuple

# Third-party modules
import motor
import tornado.ioloop
import tornado.log
import tornado.options
import tornado.web
import tornado.websocket
from dotenv import load_dotenv
from loguru import logger
from motor.motor_tornado import MotorClient, MotorDatabase
from tornado.log import LogFormatter
from tornado.options import define, options

# First-party modules
from aim.common import configmanager, utils
from aim.handlers import AIMWebSocketHandler

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2022-04-25"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.1"


# ----------------------------------------------------------------------------
# Definitions
# ----------------------------------------------------------------------------

define(
    "environment", default="development", help="Runtime environment", type=str
)
define("name", default="aim-dev", help="Instance name", type=str)
define("port", default=8888, help="Port to listen on", type=int)
define(
    "data_inputs_dir",
    default=None,
    help="Directory to store input files",
    type=Path,
)
define(
    "data_results_dir",
    default=None,
    help="Directory to store result files",
    type=Path,
)
define("database_uri", default=None, help="Database URI", type=str)
# In addition, Tornado provides built-in support for the "logging" (level) option


# ----------------------------------------------------------------------------
# Take environment variables from .env
# ----------------------------------------------------------------------------

load_dotenv()


# ----------------------------------------------------------------------------
# Functions
# ----------------------------------------------------------------------------


def parse_environ_options() -> None:
    port = os.environ.get("PORT")
    data_inputs_dir = os.environ.get("DATA_INPUTS_DIR")
    data_results_dir = os.environ.get("DATA_RESULTS_DIR")

    if os.environ.get("ENVIRONMENT"):
        options["environment"] = os.environ.get("ENVIRONMENT")
    if os.environ.get("NAME"):
        options["name"] = os.environ.get("NAME")
    if port:
        options["port"] = int(port)
    if data_inputs_dir:
        options["data_inputs_dir"] = Path(data_inputs_dir)
    if data_results_dir:
        options["data_results_dir"] = Path(data_results_dir)

    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_NAME = os.environ.get("DB_NAME")
    if DB_USER and DB_PASS and DB_HOST and DB_PORT and DB_NAME:
        options[
            "database_uri"
        ] = f"mongodb://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource=admin"


def make_app() -> Tuple[MotorDatabase, tornado.web.Application]:
    client: MotorClient = motor.motor_tornado.MotorClient(options.database_uri)
    db: MotorDatabase = client.get_database()
    settings: Dict[str, Any] = {
        "db": db,
        "debug": True if options.environment == "development" else False,
        "websocket_max_message_size": 5242880,  # 5 MB
    }
    return (
        db,
        tornado.web.Application(
            handlers=[
                (r"/ws", AIMWebSocketHandler),
            ],
            **settings,
        ),
    )


def set_tornado_logging() -> None:
    """
    Tornado root formatter settings.
    """
    for handler in logging.getLogger().handlers:
        handler.setLevel(configmanager.options.loguru_level)  # type: ignore
        formatter: LogFormatter = LogFormatter(
            fmt="%(color)s%(asctime)s.%(msecs)03dZ | %(levelname)s     | %(module)s:%(funcName)s:%(lineno)d | %(end_color)s%(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
            color=True,
        )
        setattr(formatter, "converter", time.gmtime)
        handler.setFormatter(formatter)


def main() -> None:
    configmanager.options = configmanager.parser.parse_known_args()[
        0
    ]  # Get known options, i.e., Namespace from the tuple

    # Parse options
    tornado.options.parse_command_line()

    # Configure Loguru logger
    configmanager.database_sink = lambda msg: db["errors"].insert_one(
        {"error": msg}
    )
    utils.configure_loguru_logger()

    # Configure other loggers
    set_tornado_logging()
    logging.getLogger("tensorflow").setLevel(
        logging.CRITICAL
    )  # Suppress Tensorflow logs

    # Use environment variables to override options
    parse_environ_options()

    # Make application
    db, app = make_app()
    app.listen(options.port)
    logger.info(
        "Server '{}' in {} environment is listening on http://localhost:{}".format(
            options.name, options.environment, options.port
        )
    )

    # Start application
    tornado.ioloop.IOLoop.current().start()


# ----------------------------------------------------------------------------
# Application
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
