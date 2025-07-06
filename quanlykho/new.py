from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="quanlykho_moi"
    )

@app.route("/")
def home():
    return "Flask backend is running!"

@app.route("/getTable", methods=["GET"])
def get_table():
    con = get_db_connection()
    cursor = con.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    cursor.close()
    con.close()
    table_name = [table[0] for table in tables]
    return jsonify({"tables": table_name}), 200

@app.route("/api/hanghoa", methods=["GET"])
def get_hanghoa():
    con = get_db_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM HANGHOA;")
    data = cursor.fetchall()
    cursor.close()
    con.close()
    return jsonify(data), 200

@app.route("/api/hanghoa", methods=["POST"])
def add_hanghoa():
    data = request.get_json()
    con = get_db_connection()
    cursor = con.cursor()
    try:
        cursor.execute(
            "INSERT INTO HANGHOA (MaHH, TenHH, Loai, DonVi, GiaNhap, GiaBan, SoLuongTon) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (data["MaHH"], data["TenHH"], data["Loai"], data["DonVi"], data["GiaNhap"], data["GiaBan"], data["SoLuongTon"])
        )
        con.commit()
        cursor.close()
        con.close()
        return jsonify({"success": True}), 201  
    except Exception as e:
        con.rollback()
        cursor.close()
        con.close()
        return jsonify({"error": str(e)}), 400

@app.route("/api/hanghoa/<mahh>", methods=["PUT"])
def update_hanghoa(mahh):
    data = request.get_json()
    con = get_db_connection()
    cursor = con.cursor()
    try:
        cursor.execute(
            "UPDATE HANGHOA SET TenHH=%s, Loai=%s, DonVi=%s, GiaNhap=%s, GiaBan=%s, SoLuongTon=%s WHERE MaHH=%s",
            (data["TenHH"], data["Loai"], data["DonVi"], data["GiaNhap"], data["GiaBan"], data["SoLuongTon"], mahh)
        )
        con.commit()
        cursor.close()
        con.close()
        return jsonify({"success": True}), 200
    except Exception as e:
        con.rollback()
        cursor.close()
        con.close()
        return jsonify({"error": str(e)}), 400

@app.route("/api/hanghoa/<mahh>", methods=["DELETE"])
def delete_hanghoa(mahh):
    con = get_db_connection()
    cursor = con.cursor()
    try:
        cursor.execute("DELETE FROM HANGHOA WHERE MaHH=%s", (mahh,))
        con.commit()
        cursor.close()
        con.close()
        return jsonify({"success": True}), 200
    except Exception as e:
        con.rollback()
        cursor.close()
        con.close()
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    print("connecting to database...")
    app.run(debug=True)
