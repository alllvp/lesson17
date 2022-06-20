from marshmallow import Schema, fields


class MovieSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    trailer = fields.String()
    year = fields.Integer()
    rating = fields.Float()
    genre_id = fields.Integer()
    director_id = fields.Integer()


class DirectorSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class GenreSchema(Schema):
    id = fields.Integer()
    name = fields.String()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)
