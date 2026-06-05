import json
import pytest
import app as library_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    test_file = tmp_path / "test_books.json"
    test_books = [
        {"id": 1, "title": "The Hobbit", "author": "J. R. R. Tolkien", "year": 1937},
        {"id": 2, "title": "1984", "author": "George Orwell", "year": 1949}
    ]
    test_file.write_text(json.dumps(test_books), encoding="utf-8")

    monkeypatch.setattr(library_app, "DATA_FILE", str(test_file))
    library_app.app.config["TESTING"] = True

    with library_app.app.test_client() as client:
        yield client


def test_get_books(client):
    response = client.get("/books")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["title"] == "The Hobbit"


def test_get_book_by_id_success(client):
    response = client.get("/books/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["author"] == "J. R. R. Tolkien"


def test_get_book_by_id_not_found(client):
    response = client.get("/books/99")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Book not found"


def test_create_book_success(client):
    response = client.post("/books", json={
        "title": "Dune",
        "author": "Frank Herbert",
        "year": 1965
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 3
    assert data["title"] == "Dune"

    all_books = client.get("/books").get_json()
    assert len(all_books) == 3


def test_create_book_missing_field(client):
    response = client.post("/books", json={
        "title": "Dune",
        "author": "Frank Herbert"
    })
    assert response.status_code == 400
    assert "Missing field" in response.get_json()["error"]


def test_create_book_no_data(client):
    response = client.post("/books", json=None)
    assert response.status_code == 400


def test_delete_book_success(client):
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Book deleted successfully"

    response_after_delete = client.get("/books/1")
    assert response_after_delete.status_code == 404


def test_delete_book_not_found(client):
    response = client.delete("/books/99")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Book not found"
