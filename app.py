from flask import Flask, request, jsonify, render_template
import pymysql

app = Flask(__name__)

# Konfigurasi Database
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '' # Sesuaikan dengan password MySQL Anda (kosongkan jika pakai XAMPP default)
DB_NAME = 'kampus'

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Route untuk menampilkan halaman HTML
@app.route('/')
def index():
    return render_template('index.html')

# ==========================================
# RESTFUL API ENDPOINTS
# ==========================================

# READ - Mengambil semua data mahasiswa
@app.route('/api/mahasiswa', methods=['GET'])
def get_mahasiswa():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mahasiswa ORDER BY id DESC")
    mahasiswa = cursor.fetchall()
    conn.close()
    return jsonify(mahasiswa)

# CREATE - Menambah data mahasiswa baru
@app.route('/api/mahasiswa', methods=['POST'])
def add_mahasiswa():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO mahasiswa (nim, nama, jurusan) VALUES (%s, %s, %s)"
        cursor.execute(sql, (data['nim'], data['nama'], data['jurusan']))
        conn.commit()
        return jsonify({"message": "Data berhasil ditambahkan!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

# UPDATE - Mengubah data mahasiswa berdasarkan ID
@app.route('/api/mahasiswa/<int:id>', methods=['PUT'])
def update_mahasiswa(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "UPDATE mahasiswa SET nim=%s, nama=%s, jurusan=%s WHERE id=%s"
    cursor.execute(sql, (data['nim'], data['nama'], data['jurusan'], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Data berhasil diubah!"})

# DELETE - Menghapus data mahasiswa berdasarkan ID
@app.route('/api/mahasiswa/<int:id>', methods=['DELETE'])
def delete_mahasiswa(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mahasiswa WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Data berhasil dihapus!"})

if __name__ == '__main__':
    app.run(debug=True)