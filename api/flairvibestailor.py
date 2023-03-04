#!/usr/bin/python3
"""handles caching and renders to the flair vibes tailor template file"""
from api import fvt_views
from uuid import uuid4
from flask import render_template

@fvt_views.route('/fvt', methods=['GET'], strict_slashes=False)
def flairvibes():
    """gives the webpage a cache id and renders it to the main html template"""
    cache_id = uuid4()
    return render_template('flairvibestailor.html', cache_id=cache_id)


