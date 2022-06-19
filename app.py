# app.py
from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}
db = SQLAlchemy(app)

api = Api(app)
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')


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


class MovieSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    trailer = fields.String()
    year = fields.Integer()
    rating = fields.Float()
    genre_id = fields.Integer()
    director_id = fields.Integer()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        movies_selected = db.session.query(Movie)
        if director_id:
            movies_selected = movies_selected.filter(Movie.director_id == director_id)
        if genre_id:
            movies_selected = movies_selected.filter(Movie.genre_id == genre_id)
        return movies_schema.dump(movies_selected.all()), 200


@movies_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid):
        return movie_schema.dump(Movie.query.get(uid)), 200


@directors_ns.route('/')
class DirectorsView(Resource):
    def post(self):
        req_json = request.json
        db.session.add(Director(**req_json))
        db.session.commit()
        return '', 201


@directors_ns.route('/<int:uid>')
class DirectorView(Resource):
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
    def post(self):
        req_json = request.json
        db.session.add(Genre(**req_json))
        db.session.commit()
        return '', 201

@genres_ns.route('/<int:uid>')
class GenreView(Resource):
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
