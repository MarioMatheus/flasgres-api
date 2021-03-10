from flask import Blueprint, request
from flasgres.auth import auth_required
from . import service

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')

@usuario_bp.route('', methods=['GET'])
@auth_required
def get_usuarios():
    return service.get_usuarios()

@usuario_bp.route('', methods=['POST'])
def add_usuario():
    return service.add_usuario(request.json), 201

@usuario_bp.route('/<int:usuario_id>', methods=['GET', 'PUT', 'DELETE'])
@auth_required
def get_usuario(usuario_id):
    if request.method == 'GET':
        return service.get_usuario(usuario_id)
    if request.method == 'PUT':
        return service.update_usuario(usuario_id, request.json)
    service.delete_usuario(usuario_id)
    return '', 204
