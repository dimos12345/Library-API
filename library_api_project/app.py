from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

DATA_FILE = os.environ.get("DATA_FILE", "books.json")


def load_books():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_books(books):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(books, file, ensure_ascii=False, indent=4)


@app.route("/books", methods=["GET"])
def get_books():
    books = load_books()
    return jsonify(books), 200


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book_by_id(book_id):
    books = load_books()
    for book in books:
        if book["id"] == book_id:
            return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404


@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["title", "author", "year"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    books = load_books()
    new_id = max([book["id"] for book in books], default=0) + 1

    new_book = {
        "id": new_id,
        "title": data["title"],
        "author": data["author"],
        "year": data["year"]
    }

    books.append(new_book)
    save_books(books)

    return jsonify(new_book), 201


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    books = load_books()

    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            save_books(books)
            return jsonify({"message": "Book deleted successfully"}), 200

    return jsonify({"error": "Book not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
