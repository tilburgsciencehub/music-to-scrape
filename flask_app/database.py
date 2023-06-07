import os
from flask_sqlalchemy import SQLAlchemy

# Get the absolute path to the Flask app file
app_dir = os.path.abspath(os.path.dirname(__file__))

# Construct the path to the database file
db_path = os.path.join(app_dir, 'apistoscrape.db')

# Create the SQLAlchemy database object
db = SQLAlchemy()

def init_app(app):
    # Set the database URI in Flask app configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    # Initialize the database with the Flask app
    db.init_app(app)
