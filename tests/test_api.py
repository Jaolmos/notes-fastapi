from fastapi.testclient import TestClient

def test_create_note(client):
    """Test para crear una nota"""
    response = client.post(
        "/api/notes/",
        json={
            "title": "Test Note",
            "content": "Test Content"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "Test Content"
    assert "id" in data

def test_get_notes(client):
    """Test para obtener todas las notas"""
    # Primero creamos una nota
    client.post(
        "/api/notes/",
        json={
            "title": "Test Note",
            "content": "Test Content"
        }
    )
    
    response = client.get("/api/notes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_single_note(client):
    """Test para obtener una nota específica"""
    # Crear nota
    create_response = client.post(
        "/api/notes/",
        json={
            "title": "Test Note",
            "content": "Test Content"
        }
    )
    note_id = create_response.json()["id"]
    
    # Obtener la nota
    response = client.get(f"/api/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "Test Content"

def test_update_note(client):
    """Test para actualizar una nota"""
    # Crear nota
    create_response = client.post(
        "/api/notes/",
        json={
            "title": "Test Note",
            "content": "Test Content"
        }
    )
    note_id = create_response.json()["id"]
    
    # Actualizar nota
    response = client.put(
        f"/api/notes/{note_id}",
        json={
            "title": "Updated Note",
            "content": "Updated Content"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Note"
    assert data["content"] == "Updated Content"

def test_delete_note(client):
    """Test para eliminar una nota"""
    # Crear nota
    create_response = client.post(
        "/api/notes/",
        json={
            "title": "Test Note",
            "content": "Test Content"
        }
    )
    note_id = create_response.json()["id"]
    
    # Eliminar nota
    response = client.delete(f"/api/notes/{note_id}")
    assert response.status_code == 204

    # Verificar que la nota no existe
    get_response = client.get(f"/api/notes/{note_id}")
    assert get_response.status_code == 404