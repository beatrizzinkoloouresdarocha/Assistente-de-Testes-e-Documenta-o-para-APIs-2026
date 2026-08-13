import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_status_code_get_posts():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200

def test_estrutura_dados_post():
    response = requests.get(f"{BASE_URL}/posts/1")
    dados = response.json()
    assert response.status_code == 200
    assert dados["id"] == 1
    assert "title" in dados

def test_criar_novo_post():
    payload = {
        "title": "Teste de API",
        "body": "Conteudo de teste",
        "userId": 1
    }
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    dados = response.json()
    assert response.status_code == 201
    assert dados["title"] == payload["title"]
