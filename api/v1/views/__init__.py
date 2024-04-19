#!/usr/bin/python3
"""
This __init__ provides blueprint to 
configure routes across this app.
"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")


# Wildcard import to avoid circular import errors later
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
