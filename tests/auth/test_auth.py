def test_login_by_email(client):
    body = dict(login='beltranodela@example.com', senha='beltrano')
    res = client.post('/auth/login', json=body)
    assert res.json['nome'] == 'Beltrano de Lá'

def test_login_by_cpf(client):
    body = dict(login='000.000.000-00', senha='beltrano')
    res = client.post('/auth/login', json=body)
    assert res.json['nome'] == 'Beltrano de Lá'

def test_login_by_pis(client):
    body = dict(login='000.00000.00-0', senha='beltrano')
    res = client.post('/auth/login', json=body)
    assert res.json['nome'] == 'Beltrano de Lá'

def test_login_with_wrong_credentials(client):
    body = dict(login='beltranodela@example.com', senha='errada')
    res = client.post('/auth/login', json=body)
    assert res.status_code == 401
    assert res.json['description'] == 'Email ou Senha Inválidos'
