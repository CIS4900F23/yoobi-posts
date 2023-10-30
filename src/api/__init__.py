"""Initializes our API blueprint for our Flask app"""
import os
from flask import Blueprint
from flask_restx import Api
from src.api.health import api as health_ns
from src.api.posts import api as posts_ns
from src.api.plot import api as plot_ns

# Create an API blueprint
api_bp = Blueprint("api", __name__)

# Create an API object with a title and description
api = Api(api_bp, title="Flask REST API", description="A RESTapi built with Flask")

# Add api namespaces to the api object that was created
api.add_namespace(health_ns)
api.add_namespace(posts_ns)
api.add_namespace(plot_ns)
