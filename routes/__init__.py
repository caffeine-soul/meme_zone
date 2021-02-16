from flask import Blueprint

routes = Blueprint("routes", __name__, static_folder="static", template_folder="templates")

from .meme_stream import *