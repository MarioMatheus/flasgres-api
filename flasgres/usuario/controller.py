from datetime import timedelta
from flask import Blueprint, request, make_response
from flasgres.auth import auth_required, service as auth_service
from flasgres.util.exception import BusinessException
from . import service

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')

def user_json(usuario):
    endereco_json = usuario.endereco.json()
    usuario_json = usuario.json()
    usuario_json['endereco'] = endereco_json
    return usuario_json

@usuario_bp.route('', methods=['GET'])
@auth_required
def get_usuarios():
    return service.get_usuarios()

@usuario_bp.route('', methods=['POST'])
def add_usuario():
    usuario_data = request.json
    if 'oauth' not in usuario_data:
        usuario_data['oauth'] = False
    if 'senha' not in usuario_data and not usuario_data['oauth']:
        raise BusinessException({ 'info': 'Senha é requerida' })
    if 'senha' in usuario_data and usuario_data['oauth']:
        usuario_data.pop('senha')
    usuario = service.add_usuario(usuario_data)
    response = make_response(user_json(usuario), 201)
    if not usuario_data['oauth']:
        token = auth_service.get_token_from(usuario)
        response.set_cookie('session', token, max_age=timedelta(hours=24), samesite='None', secure=True)
    return response

@usuario_bp.route('/<int:usuario_id>', methods=['GET', 'PUT', 'DELETE'])
@auth_required
def get_usuario(usuario_id):
    if request.method == 'GET':
        usuario = service.get_usuario(usuario_id)
        return user_json(usuario)
    if request.method == 'PUT':
        return user_json(service.update_usuario(usuario_id, request.json))
    service.delete_usuario(usuario_id)
    return '', 204

@usuario_bp.route('/oauth-check/<email>', methods=['GET'])
def check_usuario_ext(email):
    print(service.get_usuario_ext(email))
    return { 'result': service.get_usuario_ext(email) is not None }

@usuario_bp.route('/oauth/<email>', methods=['GET'])
@auth_required
def get_usuario_ext(email):
    return user_json(service.get_usuario_ext(email))
