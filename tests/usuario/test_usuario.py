def test_get_usuarios_without_session(client):
    res = client.get('/usuario', headers=dict(auth_test='test_get_usuarios_without_session'))
    assert res.status_code == 401
    assert res.json['description'] == 'Email ou Senha Inválidos'
    assert res.json['info'] == 'Sessão não encontrada'

def test_get_usuarios(client):
    res = client.get('/usuario')
    usuarios = list(map(lambda usuario: usuario['nome'], res.json))
    assert ['Beltrano de Lá'] == usuarios

def test_get_usuario(client):
    res = client.get('/usuario/1')
    assert res.json['nome'] == 'Beltrano de Lá'

def test_add_usuario(client):
    body = dict(
        nome='Novo Cliente',
        email='novocliente@example.com',
        senha='cliente',
        cpf='000.000.000-11',
        pis='000.00000.00-1',
        endereco=dict(
            rua='Rua Setentrional',
            numero=1000,
            cep='00000-111',
            complemento='Prox. Polo',
            municipio='Fortaleza',
            estado='Ceara',
            pais='Brasil'
        )
    )
    res = client.post('/usuario', json=body)
    assert 'id' in res.json
    assert 'senha' not in res.json
    assert res.json['nome'] == 'Novo Cliente'

def test_update_usuario(client):
    body = dict(
        nome='Beltrano [ATUALIZADO]',
        email='beltranoatualizado@example.com',
        cpf='000.000.000-00',
    )
    res = client.put('/usuario/1', json=body)
    assert res.json['id'] == 1
    assert res.json['nome'] == 'Beltrano [ATUALIZADO]'
    assert res.json['email'] == 'beltranoatualizado@example.com'
    assert res.json['cpf'] == '000.000.000-00'
    assert res.json['pis'] == '000.00000.00-0'

def test_delete_usuario(client):
    res = client.delete('/usuario/1')
    assert res.status_code == 204
