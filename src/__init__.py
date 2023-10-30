from flask import Flask
from flask_cors import CORS

# Import API Blueprint object created in api/__init__.py
from src.api import api_bp

def create_app():
    """_summary_

    Args:
        script_info (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """

    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object("src.config.DevelopmentConfig")

    # Register the blueprint to the Flask object (app) with a url route
    app.register_blueprint(api_bp, url_prefix="/api")

    # Set flask host to be open and set port to 8080
    app.run(host="0.0.0.0", port=8080)

    return app