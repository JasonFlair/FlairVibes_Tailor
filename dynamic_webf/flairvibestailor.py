#!/usr/bin/python3
"""handles caching and renders to the template file"""
from flask import Flask, render_template
from uuid import uuid4

app = Flask(__name__)

@app.route('/fvt', methods=['GET'], strict_slashes=False)
def flairvibes():
    """gives the webpage a cache id and renders it to the main html template"""
    cache_id = uuid4()
    return render_template('flairvibestailor.html', cache_id=cache_id)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5001)