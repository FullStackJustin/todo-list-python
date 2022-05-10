"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Starships
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/characters', methods=['GET'])
def handle_characters():
    characters_query = Characters.query.all()
    all_characters =list(map(lambda character: character.serialize(), characters_query))
    return jsonify(all_characters), 200


@app.route('/characters/<int:characters_id>', methods=['GET'])
def handle__character(characters_id):
    user1 = Characters.query.get(characters_id)
    return jsonify(user1.serialize()), 200

@app.route('/starships', methods=['GET'])
def handle_starships():
    starships_query = Starships.query.all()
    all_starships =list(map(lambda starships: starships.serialize(), starships_query))
    return jsonify(all_starships), 200


# this only runs if `$ python src/main.py` is executed
    if __name__ == '__main__':
        PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
