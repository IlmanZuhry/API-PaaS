from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {
        "id": 1,
        "judul": "Pemrograman Python",
        "penulis": "Andi",
        "tahun": 2024
    },
    {
        "id": 2,
        "judul": "Dasar Database",
        "penulis": "Budi",
        "tahun": 2023
    },
    {
        "id": 3,
        "judul": "Belajar REST API",
        "penulis": "Citra",
        "tahun": 2025
    }
]


@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "Book API berhasil berjalan"
    })


@app.route("/books", methods=["GET"])
def get_books():
    return jsonify({
        "status": "success",
        "jumlah": len(books),
        "data": books
    })


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):

    for book in books:
        if book["id"] == book_id:
            return jsonify({
                "status": "success",
                "data": book
            })

    return jsonify({
        "status": "error",
        "message": "Buku tidak ditemukan"
    }), 404


@app.route("/books", methods=["POST"])
def add_book():

    data = request.get_json()

    if not data or not data.get("judul") or not data.get("penulis"):
        return jsonify({
            "status": "error",
            "message": "judul dan penulis wajib diisi"
        }), 400

    new_book = {
        "id": len(books) + 1,
        "judul": data["judul"],
        "penulis": data["penulis"],
        "tahun": data.get("tahun")
    }

    books.append(new_book)

    return jsonify({
        "status": "success",
        "message": "Buku berhasil ditambahkan",
        "data": new_book
    }), 201


if __name__ == "__main__":
    app.run(debug=True)