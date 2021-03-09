from .model import db, Usuario, Endereco

def get_usuarios():
    return Usuario.query.all()

def get_usuario(usuario_id):
    return Usuario.query.get(usuario_id)

def add_usuario(usuario_data):
    endereco = Endereco(**usuario_data['endereco'])
    usuario_data['endereco'] = endereco
    usuario = Usuario(**usuario_data)
    db.session.add(usuario)
    db.session.commit()
    return usuario

def update_usuario(usuario_id, usuario_data):
    endereco_data = usuario_data.pop('endereco')
    Usuario.query.filter_by(id=usuario_id).update(usuario_data)
    usuario = Usuario.query.get(usuario_id)
    Endereco.query.filter_by(id=usuario.endereco.id).update(endereco_data)
    db.session.commit()
    return usuario

def delete_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
