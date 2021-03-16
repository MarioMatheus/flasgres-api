from flasgres.usuario import service, model

def test_get_usuario_by_login(client):
    def match(usuario):
        return usuario is not None and usuario.nome == 'Beltrano de Lá'
    with client.app.app_context():
        usuarios = [
            service.get_usuario_by_login('beltranodela@example.com'),
            service.get_usuario_by_login('000.000.000-00'),
            service.get_usuario_by_login('000.00000.00-0'),
        ]
        assert all(match(usuario) for usuario in usuarios)

def test_update_usuario(client):
    data = dict(nome='Beltrano [ATUALIZADO]', endereco=dict(numero=100))
    with client.app.app_context():
        old_usuario = model.Usuario.query.get(1)
        assert old_usuario.nome == 'Beltrano de Lá'
        assert old_usuario.endereco.numero == 2393
        usuario = service.update_usuario(1, data)
        assert usuario.nome == 'Beltrano [ATUALIZADO]'
        assert usuario.endereco.numero == 100

def test_delete_usuario(client):
    with client.app.app_context():
        usuario = model.Usuario.query.get(1)
        assert usuario is not None
        service.delete_usuario(usuario.id)
        assert model.Usuario.query.get(1) is None
