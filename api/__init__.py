from flask import Blueprint

stats_endpoint = Blueprint('stats_endpoint', __name__, template_folder='templates')

from . import stats