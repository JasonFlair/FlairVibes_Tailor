#!/usr/bin/python3
"""handles caching and renders to the landing page template file"""
from api import fvt_views
from flask import render_template
from uuid import uuid4


@fvt_views.route('/fvtlp', methods=['GET'], strict_slashes=False)
def flairvibeslp():
    """gives the webpage a cache id and renders it to the main html template"""
    cache_id = uuid4()
    return render_template('fvtlandingpage.html', cache_id=cache_id)

