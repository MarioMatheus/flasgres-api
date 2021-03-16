import pytest
from sqlalchemy.sql import text
from flasgres import create_app, db

def execute_init_sql():
    sql_query = open('tests/_data/_init_data.sql', 'r').read()
    db.engine.execute(text(sql_query))

@pytest.fixture
def client():
    app = create_app('config.TestingConfig')
    with app.app_context():
        db.create_all()
        execute_init_sql()
    with app.test_client() as _client:
        _client.app = app
        yield _client
    with app.app_context():
        db.drop_all()
