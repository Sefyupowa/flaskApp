import os
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

# MySQL configuration (updated for Kubernetes)
root_db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'mydb'  # MySQL service name in Kubernetes
}

# MySQL config for connecting to the actual database
db_config = {
    'user': 'root',
    'password': 'password',
    'host': 'mydb',
    'database': 'testdb'
}

# Function to create the database and the table if they don't exist
def init_db():
    # Step 1: Connect to MySQL without specifying a database to create 'testdb'
    connection = mysql.connector.connect(**root_db_config)
    cursor = connection.cursor()

    # Create the database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS testdb")
    cursor.close()
    connection.close()

    # Step 2: Now connect to the 'testdb' database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Create the 'words' table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INT AUTO_INCREMENT PRIMARY KEY,
            word VARCHAR(255) NOT NULL
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()

@app.route('/add_word', methods=['POST'])
def add_word():
    word = request.json.get('word')
    if not word:
        return jsonify({"error": "No word provided"}), 400

    # Connect to MySQL
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # Insert the word into the 'words' table
        cursor.execute("INSERT INTO words (word) VALUES (%s)", (word,))
        connection.commit()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({"message": "Word added successfully!"}), 201

@app.route('/words', methods=['GET'])
def get_words():
    # Connect to MySQL
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        # Retrieve all words from the 'words' table
        cursor.execute("SELECT word FROM words")
        words = cursor.fetchall()
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

    # Convert the result into a list of words
    words_list = [word[0] for word in words]

    return jsonify({"words": words_list})

@app.route('/')
def hello_world():
    return f'Hello World! from {os.getenv("ENVIRONMENT", "notSet")}'

if __name__ == '__main__':
    init_db()  # Initialize the DB and create tables
    app.run(host="0.0.0.0", port=8080)
