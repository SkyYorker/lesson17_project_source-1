# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from shemas import movie_schema, movies_schema, director_schema, directors_schema, genre_schema, genres_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


 
api = Api(app)
movies_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')

@movies_ns.route('/')
class MoveisView(Resource):

    def get(self):
        all_movies = Movie.query.all()
        did = request.args.get('director_id')
        gid = request.args.get('genre_id')
        if len(request.args) == 2: # rfr
            all_movies = Movie.query.filter(Movie.director_id == did, Movie.genre_id == gid) 
            return movies_schema.dump(all_movies)
        if 'director_id' in request.args:
            all_movies = Movie.query.filter(Movie.director_id == did)
            return movies_schema.dump(all_movies)
        if 'genre_id' in request.args:
            all_movies = Movie.query.filter(Movie.genre_id == gid)
            return movies_schema.dump(all_movies)
        return movies_schema.dump(all_movies)
    
    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201

@movies_ns.route('/<int:mid>')
class MoveieView(Resource):

    def get(self, mid: int):
        movie = Movie.query.get(mid)
        return movie_schema.dump(movie), 200

    def put(self, mid):
        movie = Movie.query.get(mid)
        req_json = request.json
        movie.title = req_json.get('title')
        movie.description = req_json.get('description')
        movie.trailer = req_json.get('trailer')
        movie.year = req_json.get('year')
        movie.rating = req_json.get('rating')
        movie.genre_id = req_json.get('genre_id')
        movie.director_id = req_json.get('director_id')
        db.session.add(movie)
        db.session.commit()
        return "", 204

    def delete(self, mid: int):
        movie = Movie.query.get(mid)
        db.session.delete(movie)
        db.session.commit()
        return "", 204


@director_ns.route('/')
class DirectorsView(Resource):

    def get(self):
        director = Director.query.all()
        return directors_schema.dump(director), 200

    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201


@director_ns.route('/<int:did>')
class DirectorsView(Resource):
    
    def get(self, did: int):
        director = Director.query.get(did)
        return director_schema.dump(director), 200

    def put(self, did):
        director = Director.query.get(did)
        req_json = request.json
        director.name = req_json.get('name')
        db.session.add(director)
        db.session.commit()
        return "", 204

    def delete(self, did: int):
        director = Director.query.get(did)
        db.session.delete(director)
        db.session.commit()
        return "", 204


@genre_ns.route('/')
class GenresView(Resource):

    def get(self):
        all_genres = Genre.query.all()
        return genres_schema.dump(all_genres), 200

    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201


@genre_ns.route('/<int:gid>')
class GenresView(Resource):

    def get(self, gid: int):
        genre = Genre.query.get(gid)
        return genre_schema.dump(genre), 200

    def put(self, gid):
        genre = Genre.query.get(gid)
        req_json = request.json
        genre = req_json.get('name')
        db.session.add(genre)
        db.session.commit()
        return "", 204

    def delete(self, gid: int):
        genre = Genre.query.get(gid)
        db.session.delete(genre)
        db.session.commit()
        return "", 204    

if __name__ == '__main__':
    app.run(debug=True)