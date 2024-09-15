import os
from flask import Flask

app = Flask(__name__)

# Retrieve environment name from the environmental variable 'ENVIRONMENT', default to 'dev' if not set
environment = os.getenv('ENVIRONMENT', 'notSet')

@app.route('/')
def hello_world():
    return f'Hello World! from {environment}'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)