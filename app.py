from flask import Flask, jsonify, request
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


def get_db_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "Book API berhasil berjalan"
    })


@app.route("/books", methods=["GET"])
def get_books():

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, judul, penulis, tahun
            FROM books
            ORDER BY id
        """)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        books = []

        for row in rows:
            books.append({
                "id": row[0],
                "judul": row[1],
                "penulis": row[2],
                "tahun": row[3]
            })

        return jsonify({
            "status": "success",
            "jumlah": len(books),
            "data": books
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, judul, penulis, tahun
            FROM books
            WHERE id = %s
        """, (book_id,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row is None:
            return jsonify({
                "status": "error",
                "message": "Buku tidak ditemukan"
            }), 404

        return jsonify({
            "status": "success",
            "data": {
                "id": row[0],
                "judul": row[1],
                "penulis": row[2],
                "tahun": row[3]
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/books", methods=["POST"])
def add_book():

    try:
        data = request.get_json()

        judul = data.get("judul")
        penulis = data.get("penulis")
        tahun = data.get("tahun")

        if not judul or not penulis or not tahun:
            return jsonify({
                "status": "error",
                "message": "judul, penulis, dan tahun wajib diisi"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO books (judul, penulis, tahun)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (judul, penulis, tahun))

        book_id = cursor.fetchone()[0]

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "status": "success",
            "message": "Buku berhasil ditambahkan",
            "id": book_id
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )