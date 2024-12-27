from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# MySQL database connection
try:
    db = mysql.connector.connect(
        host="127.0.0.1",  # replace with your MySQL host
        user="root",  # replace with your MySQL username
        password="root",  # replace with your MySQL password
        database="cl"  # replace with your database name
    )
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

@app.route("/", methods=["GET"])
def home():
    return {"message": "Localhost is running"}

@app.route("/users", methods=["GET"])
def get_users():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ul")
        users = cursor.fetchall()
        if not users:
            return jsonify({"message": "No users found"}), 404
        return jsonify(users), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route("/users", methods=["POST"])
def add_user():
    try:
        data = request.json
        name = data.get("name")
        email = data.get("email")
        phone_no = data.get("phone_no")

        if not name or not email or not phone_no:
            return jsonify({"error": "Missing required fields"}), 400

        cursor = db.cursor()
        query = "INSERT INTO ul (name, email, phone_no) VALUES (%s, %s, %s)"
        values = (name, email, phone_no)
        cursor.execute(query, values)
        db.commit()

        # Get the auto-incremented ID of the newly inserted user
        user_id = cursor.lastrowid
        return jsonify({"message": "User added successfully", "user_id": user_id}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route("/users/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    try:
        data = request.json
        fields = []
        values = []

        if "name" in data:
            fields.append("name = %s")
            values.append(data["name"])
        if "email" in data:
            fields.append("email = %s")
            values.append(data["email"])
        if "phone_no" in data:
            fields.append("phone_no = %s")
            values.append(data["phone_no"])

        if not fields:
            return jsonify({"error": "No fields to update"}), 400

        values.append(user_id)
        query = f"UPDATE ul SET {', '.join(fields)} WHERE id = %s"
        cursor = db.cursor()
        cursor.execute(query, values)
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "User not found"}), 404

        return jsonify({"message": "User updated successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        cursor = db.cursor()
        query = "DELETE FROM ul WHERE id = %s"
        cursor.execute(query, (user_id,))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"message": "User not found"}), 404

        return jsonify({"message": "User deleted successfully"}), 200
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

if __name__ == "__main__":
    app.run(debug=True)
