# app.py
from flask import Flask, request
from flask_restx import Api, Resource
from models import Movie, Director, Genre
from setup_db import db
from schemas import movies_schema, movie_schema, genres_schema, directors_schema, director_schema, genre_schema
import utils

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}

db.init_app(app)

api = Api(app)
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 5))
        movies_selected = db.session.query(Movie)
        if director_id:
            movies_selected = movies_selected.filter(Movie.director_id == director_id)
        if genre_id:
            movies_selected = movies_selected.filter(Movie.genre_id == genre_id)
        movies_selected = utils.pagination(movies_selected, page, page_size).all()
        return movies_schema.dump(movies_selected), 200

    def post(self):
        req_json = request.json
        db.session.add(Movie(**req_json))
        db.session.commit()
        return '', 201


@movies_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid):
        return movie_schema.dump(Movie.query.get(uid)), 200

    def put(self, uid):
        movie = Movie.query.get(uid)
        if not movie:
            return '', 404
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
        return '', 204

    def delete(self, uid: int):
        movie = Movie.query.get(uid)
        if not movie:
            return "", 404
        db.session.delete(movie)
        db.session.commit()
        return "", 204


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        return directors_schema.dump(db.session.query(Director).all()), 200

    def post(self):
        req_json = request.json
        db.session.add(Director(**req_json))
        db.session.commit()
        return '', 201


@directors_ns.route('/<int:uid>')
class DirectorView(Resource):
    def get(self, uid):
        return director_schema.dump(Director.query.get(uid)), 200

    def post(self):
        req_json = request.json
        db.session.add(Director(**req_json))
        db.session.commit()

    def put(self, uid):
        director = Director.query.get(uid)
        if not director:
            return "", 404
        req_json = request.json
        director.name = req_json.get("name")
        db.session.add(director)
        db.session.commit()
        return "", 204

    def patch(self, uid):
        director = Director.query.get(uid)
        if not director:
            return "", 404
        req_json = request.json
        if "name" in req_json:
            director.name = req_json.get("name")
        db.session.add(director)
        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        director = Director.query.get(uid)
        if not director:
            return "", 404
        db.session.delete(director)
        db.session.commit()
        return "", 204


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        return genres_schema.dump(db.session.query(Genre).all()), 200

    def post(self):
        req_json = request.json
        db.session.add(Genre(**req_json))
        db.session.commit()
        return '', 201

@genres_ns.route('/<int:uid>')
class GenreView(Resource):
    def get(self, uid):
        return genre_schema.dump(Genre.query.get(uid)), 200

    def put(self, uid):
        genre = Genre.query.get(uid)
        if not genre:
            return "", 404
        req_json = request.json
        genre.name = req_json.get("name")
        db.session.add(genre)
        db.session.commit()
        return "", 204

    def patch(self, uid):
        genre = Genre.query.get(uid)
        if not genre:
            return "", 404
        req_json = request.json
        if "name" in req_json:
            genre.name = req_json.get("name")
        db.session.add(genre)
        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        genre = Genre.query.get(uid)
        if not genre:
            return "", 404
        db.session.delete(genre)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=False)
