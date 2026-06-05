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


def test_get_book_by_id(client):
    response = client.get("/books/1")
    assert response.status_code == 200


def test_create_book(client):
    response = client.post(
        "/books",
        json={
            "title": "Dune",
            "author": "Frank Herbert",
            "year": 1965
        }
    )

    assert response.status_code in [200, 201]


def test_delete_book(client):
    response = client.delete("/books/1")
    assert response.status_code == 200
