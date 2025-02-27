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
from models import db, User, Planet, People, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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
def get_user():
    user=User.query.all()
    user_serialized=([user.serialize()for user in user])
    print(user_serialized)
    return jsonify({"msg":"ok", "data":user_serialized})

@app.route('/people', methods=['GET'])
def get_people():
    people=People.query.all()
    people_serialized=([person.serialize() for person in people])
    return jsonify({"msg":"ok", "data":people_serialized})

@app.route('/people/<int:id>', methods=['GET'])
def get_peopleid(id):
    people = People.query.get(id)

 
    if people is None:
        return jsonify({"msg": f"Person with id {id} not found"}), 404  

    return jsonify({ "msg": f"One person with id: {id}", "people": people.serialize(), 
    }), 200

    


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()  
    planets_serialized = [planet.serialize() for planet in planets]  

    return jsonify({ "msg": "ok","data": planets_serialized})

@app.route('/planets/<int:id>', methods=['GET'])
def get_planetsid(id):
    planets = Planet.query.get(id)
    if planets is None:
        return jsonify({"msg": f"planet with id {id} not found"}), 404
    return jsonify({"msg": f"planet with id: {id}", "planet": planets.serialize()}), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': f.id, 'people_id': f.people_id, 'planet_id': f.planet_id} for f in favorites])

@app.route('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    existing_fav = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_fav:
        return jsonify({'message': 'Planet already in favorites'}), 400

    favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Planet added to favorites'})

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = 1
    favorite = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'People added to favorites'})

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = 1
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'message': 'Planet removed from favorites'})
    return jsonify({'message': 'Planet not found in favorites'}), 404

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = 1
    favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'message': 'People removed from favorites'})
    return jsonify({'message': 'People not found in favorites'}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
