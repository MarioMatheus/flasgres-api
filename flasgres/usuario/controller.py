from datetime import timedelta
from flask import Blueprint, request, make_response
from flasgres.auth import auth_required, service as auth_service
from . import service

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')

@usuario_bp.route('', methods=['GET'])
@auth_required
def get_usuarios():
    return service.get_usuarios()

@usuario_bp.route('', methods=['POST'])
def add_usuario():
    usuario = service.add_usuario(request.json)
    token = auth_service.get_token_from(usuario)
    response = make_response(usuario, 201)
    response.set_cookie('session', token, max_age=timedelta(hours=24))
    return response

@usuario_bp.route('/<int:usuario_id>', methods=['GET', 'PUT', 'DELETE'])
@auth_required
def get_usuario(usuario_id):
    if request.method == 'GET':
        usuario = service.get_usuario(usuario_id)
        endereco_json = usuario.endereco.json()
        usuario_json = usuario.json()
        usuario_json['endereco'] = endereco_json
        return usuario_json
    if request.method == 'PUT':
        return service.update_usuario(usuario_id, request.json)
    service.delete_usuario(usuario_id)
    return '', 204
