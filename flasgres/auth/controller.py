from flask import Blueprint, request
from . import service

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    return service.authenticate(request.json)
