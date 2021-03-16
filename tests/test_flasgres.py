def test_root(client):
    res = client.get('/')
    assert b'Hello Flasgres' in res.data
