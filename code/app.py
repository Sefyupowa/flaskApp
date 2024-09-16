import os
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

# Retrieve environment name from the environmental variable 'ENVIRONMENT', default to 'notSet' if not set
environment = os.getenv('ENVIRONMENT', 'notSet')

# MySQL configuration (Update this according to your local or cloud MySQL settings)
db_config = {
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'password'),
    'host': os.getenv('MYSQL_HOST', 'mysql-container'),
    'port': os.getenv('MYSQL_PORT', 3306),
    'database': os.getenv('MYSQL_DATABASE', 'testdb')
}

def create_table_if_not_exists():
    """Create the words table if it does not already exist."""
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS words (
        id INT AUTO_INCREMENT PRIMARY KEY,
        word VARCHAR(255) NOT NULL
    )
    """

    try:
        cursor.execute(create_table_query)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()
        connection.close()

# Create the table if it doesn't exist
create_table_if_not_exists()

# Route to insert words into MySQL database
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

# Route to retrieve all words from MySQL database
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
    return f'Hello World! from {environment}'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
