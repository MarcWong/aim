#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for the message model.
"""


# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

# Standard library modules
from typing import Any, Dict, List

# Third-party modules
from fastapi.encoders import jsonable_encoder
from pydantic.error_wrappers import ValidationError

# First-party modules
from aim.models import MessageImage, MessageURL

# ----------------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------------

__author__ = "Markku Laine"
__date__ = "2021-04-07"
__email__ = "markku.laine@aalto.fi"
__version__ = "1.0"


# ----------------------------------------------------------------------------
# Input values
# ----------------------------------------------------------------------------

input_value_message_url: Dict[str, Any] = {
    "type": "execute",
    "input": "url",
    "url": "http://aalto.fi",
    "data": None,
    "filename": None,
    "metrics": {
        "cp1": False,
        "cp2": True,
    },
}

input_value_message_image: Dict[str, Any] = {
    "type": "execute",
    "input": "image",
    "url": None,
    "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABQAAAAMgCAIAAADz+lisAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAFHhJREFUeNrs1zEBAAAIw7DNv2jQwMOVSOjXJhMA4NekIgDAsxpgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADLABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwACrAAAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMsAgAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAAbYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAywAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABNsAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYBUAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAG2AADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggEUAAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYAMMAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAATbAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAA2yAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAOsAgAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAAbYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAywCABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAANsgAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCADTAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAG2AADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggFUAAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDABcrQADAD9fQFtof4yoAAAAAElFTkSuQmCC",
    "filename": "blue_50_red_50.png",
    "metrics": {
        "cp1": False,
        "cp2": True,
    },
}

input_value_message_invalid: Dict[str, Any] = {
    "type": "execute",
    "url": None,
    "data": None,
}


# ----------------------------------------------------------------------------
# Expected results
# ----------------------------------------------------------------------------

expected_result_message_url: Dict[str, Any] = {
    "type": "execute",
    "input": "url",
    "url": "http://aalto.fi",
    "data": None,
    "filename": None,
    "metrics": {
        "cp2": True,
    },
}

expected_result_message_image: Dict[str, Any] = {
    "type": "execute",
    "input": "image",
    "url": None,
    "data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABQAAAAMgCAIAAADz+lisAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAFHhJREFUeNrs1zEBAAAIw7DNv2jQwMOVSOjXJhMA4NekIgDAsxpgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADLABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwACrAAAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMsAgAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAAbYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAywAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABNsAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYBUAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAG2AADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggEUAAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYAMMAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAATbAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAA2yAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAOsAgAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAAbYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAywCABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAANsgAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCADTAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAG2AADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggFUAAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDABcrQADAD9fQFtof4yoAAAAAElFTkSuQmCC",
    "filename": "blue_50_red_50.png",
    "metrics": {
        "cp2": True,
    },
    "raw_data": "iVBORw0KGgoAAAANSUhEUgAABQAAAAMgCAIAAADz+lisAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAFHhJREFUeNrs1zEBAAAIw7DNv2jQwMOVSOjXJhMA4NekIgDAsxpgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADLABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwACrAAAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMsAgAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAAbYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAywAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABNsAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYBUAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAG2AADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggEUAAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYAMMAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAATbAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAA2yAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAOsAgAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAAbYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAywCABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAGGAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgAMMAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMABggAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAANsgAHAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDABhgADDAAGGAAwAADgAEGAAwwABhgAMAAA4ABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAgAEGAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAEAAwwABhgADDAAYIABwAADAAYYAAwwAGCAAcAAAwAGGAAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAwwABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwAGGAAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwACAAQYAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAQADDAAGGAAMMABggAHAAAMABhgADDAAYIABwAADAAYYAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggAEAAwwABhgAMMAAYIABAAMMAAYYADDAAGCAAcAAAwAGGAAMMABggAHAAAMABhgADDAAYIABwAADgAEGAAwwABhgAMAAA4ABBgAMMAAYYADAAAOAAQYAAwwAGGAAMMAAgAEGAAMMABhgADDAAGCADTAAGGAAMMAAgAEGAAMMABhgADDAAIABBgADDAAG2AADgAEGAAMMABhgADDAAIABBgADDAAYYAAwwABggFUAAAMMAAYYADDAAGCAAQADDAAGGAAwwABggAHAAAMABhgADDAAYIABwAADAAYYAAwwAGCAAcAAA4ABBgAMMAAYYADAAAOAAQYADDAAGGAAwAADgAEGAAMMABhgADDAAIABBgADDABcrQADAD9fQFtof4yoAAAAAElFTkSuQmCC",
}

expected_result_message_invalid: List[Dict[str, Any]] = [
    {
        "loc": ("input",),
        "msg": "field required",
        "type": "value_error.missing",
    },
    {
        "loc": ("data",),
        "msg": "none is not an allowed value",
        "type": "type_error.none.not_allowed",
    },
    {
        "loc": ("filename",),
        "msg": "field required",
        "type": "value_error.missing",
    },
    {
        "loc": ("metrics",),
        "msg": "field required",
        "type": "value_error.missing",
    },
]


# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


class TestMessageModel:
    """
    A test class for the message model.
    """

    # Public methods
    def test_message_url(self) -> None:
        """
        Test message URL.
        """
        message: MessageURL = MessageURL(**input_value_message_url)
        message_data = jsonable_encoder(message)
        assert message_data == expected_result_message_url

    def test_message_image(self) -> None:
        """
        Test message image.
        """
        message: MessageImage = MessageImage(**input_value_message_image)
        message_data = jsonable_encoder(message)
        assert message_data == expected_result_message_image

    def test_message_invalid(self) -> None:
        """
        Test message invalid.
        """
        try:
            MessageImage(**input_value_message_invalid)
        except ValidationError as e:
            assert e.errors() == expected_result_message_invalid
