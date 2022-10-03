from marshmallow import Schema, fields

class MoveisSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Int()
    genre_id = fields.Int()
    genre = fields.Str()
    director_id = fields.Int()
    director = fields.Str()


class DirectorsSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenresSchema(Schema):
    id = fields.Int()
    name = fields.Str()

movie_schema = MoveisSchema()
movies_schema = MoveisSchema(many=True)

director_schema = DirectorsSchema()
directors_schema = DirectorsSchema(many=True)

genre_schema = GenresSchema()
genres_schema = GenresSchema(many=True)