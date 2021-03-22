from flask import Blueprint, request, make_response
from . import service

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    usuario, token = service.authenticate(request.json)
    response = make_response(usuario)
    response.set_cookie('session', token, **service.get_cookie_options())
    return response
