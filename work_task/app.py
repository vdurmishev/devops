from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Create users table if it doesn't exist
with sqlite3.connect('users.db', check_same_thread=False) as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS USERS
                 (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 NAME TEXT NOT NULL);''')


# Route for registering new users
@app.route('/register', methods=['POST'])
def register():
    name = request.json.get('name')
    if not name:
        return jsonify({'error': 'Please provide a name.'}), 400
    # Insert user into database
    with sqlite3.connect('users.db', check_same_thread=False) as conn:
        conn.execute("INSERT INTO USERS (NAME) VALUES (?)", (name,))
        conn.commit()
    return jsonify({'success': 'User {} registered successfully.'.format(name)})


# Route for getting all registered users
@app.route('/users', methods=['GET'])
def users():
    with sqlite3.connect('users.db', check_same_thread=False) as conn:
        cursor = conn.execute("SELECT NAME FROM USERS")
        users = [row[0] for row in cursor.fetchall()]
    return jsonify({'users': users})


if __name__ == '__main__':
    app.run(debug=True)