#!/usr/bin/python3
""" Blueprint for the flair vibes tailor API """

from flask import Blueprint

fvt_views = Blueprint('fvt_views', __name__, url_prefix='/api')

from dynamic_webf.api.flairvibestailor import *
from dynamic_webf.api.landingpage import *
from dynamic_webf.api.sub_rec import *