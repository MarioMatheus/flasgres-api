from sqlalchemy import or_
from werkzeug.security import generate_password_hash
from .model import db, Usuario, Endereco

def get_usuarios():
    return Usuario.query.all()

def get_usuario(usuario_id):
    return Usuario.query.get(usuario_id)

def get_usuario_by_login(login):
    return Usuario.query.filter(or_(
        Usuario.email == login,
        Usuario.cpf == login,
        Usuario.pis == login,
    )).first()

def add_usuario(usuario_data):
    endereco = Endereco(**usuario_data['endereco'])
    usuario_data['endereco'] = endereco
    usuario_data['senha'] = generate_password_hash(usuario_data['senha'])
    usuario = Usuario(**usuario_data)
    db.session.add(usuario)
    db.session.commit()
    return usuario

def update_usuario(usuario_id, usuario_data):
    endereco_data = {}
    if 'endereco' in usuario_data:
        endereco_data = usuario_data.pop('endereco')
    Usuario.query.filter_by(id=usuario_id).update(usuario_data)
    usuario = Usuario.query.get(usuario_id)
    if endereco_data != {}:
        Endereco.query.filter_by(id=usuario.endereco.id).update(endereco_data)
    db.session.commit()
    return usuario

def delete_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
