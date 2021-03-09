from flask import Blueprint, request
from . import service

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')

@usuario_bp.route('', methods=['GET', 'POST'])
def get_usuarios():
    if request.method == 'GET':
        return service.get_usuarios()
    return service.add_usuario(request.json), 201

@usuario_bp.route('/<int:usuario_id>', methods=['GET', 'PUT', 'DELETE'])
def get_usuario(usuario_id):
    if request.method == 'GET':
        return service.get_usuario(usuario_id)
    if request.method == 'PUT':
        return service.update_usuario(usuario_id, request.json)
    service.delete_usuario(usuario_id)
    return '', 204
