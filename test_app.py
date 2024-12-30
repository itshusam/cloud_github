import pytest
from app import app, db, Sum

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_add_sum(client):
    response = client.post('/sum', json={'result': 10})
    assert response.status_code == 201
    assert response.json['result'] == 10

def test_get_sums_by_result(client):
    client.post('/sum', json={'result': 10})
    client.post('/sum', json={'result': 20})
    response = client.get('/sum/result/10')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['result'] == 10

def test_get_sums_invalid_filter(client):
    response = client.get('/sum/result/string')
    assert response.status_code == 404  # Or 400 if handled differently

