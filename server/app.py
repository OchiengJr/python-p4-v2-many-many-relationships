#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json.compact = False

    db.init_app(app)
    Migrate(app, db)

    @app.route('/')
    def index():
        return jsonify({'message': 'Welcome to the API'})

    # Register additional blueprints/routes here

    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5555, debug=True)
