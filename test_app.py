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

def test_get_all_sums(client):
    client.post('/sum', json={'result': 10})
    client.post('/sum', json={'result': 20})
    response = client.get('/sum')
    assert response.status_code == 200
    assert len(response.json) == 2

def test_get_sums_by_result(client):
    client.post('/sum', json={'result': 10})
    client.post('/sum', json={'result': 20})
    response = client.get('/sum/result/10')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['result'] == 10

def test_get_sums_invalid_filter(client):
    response = client.get('/sum/result/abc')  # Invalid filter (auto 404 due to Flask routing)
    assert response.status_code == 404

def test_get_sums_nonexistent_result(client):
    client.post('/sum', json={'result': 10})
    response = client.get('/sum/result/99')  # Nonexistent result
    assert response.status_code == 404
    assert response.json['error'] == 'No sums found for result 99'
