#!/usr/bin/python3
""" Unified Flask Application """
from dynamic_webf.api import fvt_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(fvt_views)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5004, threaded=True)