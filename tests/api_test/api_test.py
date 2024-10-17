from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_info():
    response = client.get("/borrius_pokemon/info")
    assert response.status_code == 200
    assert '"borrius_pokemon":{"description":"Data pulled from BorriusPokedexScraper. https://github.com/nMckenryan/BorriusPokedexScraper"' in response.text


def test_read_pokemon_all():
    response = client.get("/borrius_pokemon/")
    assert response.status_code == 200  
    assert 'hoopa' in response.text

def test_read_pokemon_by_id():
    response = client.get("/borrius_pokemon/11")
    assert response.status_code == 200  
    assert 'snorunt' in response.text

def test_read_pokemon_by_name():
    response = client.get("/borrius_pokemon/name/snorunt")
    assert response.status_code == 200  
    assert 'snorunt' in response.text

def test_read_pokemon_by_types():
    response = client.get("/borrius_pokemon/types/?type1=rock&type2=dark")
    assert response.status_code == 200  
    assert 'tyranitar' in response.text
    
def test_read_pokemon_by_single_type():
    response = client.get("/borrius_pokemon/types/?type1=ice")
    assert response.status_code == 200  
    assert 'snorunt' in response.text
