#!/usr/bin/python3
""" Blueprint for the flair vibes tailor API """

from flask import Blueprint

fvt_views = Blueprint('fvt_views', __name__, url_prefix='', static_url_path='fvtstatic')

from api.flairvibestailor import *
from api.landingpage import *
from api.sub_rec import *