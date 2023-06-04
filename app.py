from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_marshmallow import Marshmallow

app = Flask(__name__)

## DB CONNECTION AREA

# set the database URI via SQLAlchemy, 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://tomato:tomato123@localhost:5432/ripe_tomatoes_db'

# to avoid the deprecation warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#create the database object
db = SQLAlchemy(app)

ma = Marshmallow(app)

# CLI COMMANDS AREA

# create app's cli command named create, then run it in the terminal as "flask create", 
# it will invoke create_db function
@app.cli.command("create")
def create_db():
    db.drop_all()
    db.create_all()
    print("Tables created for Phillip")

@app.cli.command('seed')
def seed_db():
    # Create an instance of the card model in memory
    movies = [
        Movie(
            title = 'The Shawshank Redemption', 
            genre = "Drama",
            length_in_mins = 142,
            release_year = 1994
        ),
        Movie(
            title = 'The Conjuring', 
            genre = "Horror",
            length_in_mins = 112,
            release_year = 2013
        )
    ]

    actors = [
        Actor(
            f_name = "Patrick", 
            l_name = "Wilson",
            gender = 'Male',
            country = "USA",
            dob = '1973/07/03'
        ),
        Actor(
            f_name = "Ron", 
            l_name = "Livingston",
            gender = 'Male',
            country = "USA",
            dob = '1967/06/05'
        ),
        Actor(
            f_name = "Tim", 
            l_name = "Robbins",
            gender = 'Male',
            country = "USA",
            dob = '1958/10/16'
        ),
        Actor(
            f_name = "Morgan", 
            l_name = "Freeman",
            gender = 'Male',
            country = "USA",
            dob = '1937/07/01'
        )
    ]


    # Truncate the Card table
    db.session.query(Movie).delete()
    db.session.query(Actor).delete()
    # Add the card to the session (transaction)
    # db.session.add(card)
    db.session.add_all(movies)
    db.session.add_all(actors)

    # Commit the tranaction to the database
    db.session.commit()
    print('Models seeded for Phillip')

@app.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped for Phillip") 

# MODELS AREA
class Movie(db.Model):
    # define the table name for the db
    __tablename__= "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    genre = db.Column(db.String(100))
    length_in_mins = db.Column(db.Integer())
    release_year = db.Column(db.Integer())

class Actor(db.Model):
    # define the table name for the db
    __tablename__= "actors"

    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.Text())
    l_name = db.Column(db.Text())
    gender = db.Column(db.String(50))
    country = db.Column(db.Text())
    dob = db.Column(db.Date())

# SCHEMAS AREA

#create the Card Schema with Marshmallow, it will provide the serialization needed for converting the data into JSON
class MovieSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "title", "genre", "length_in_mins", "release_year")

#single card schema, when one card needs to be retrieved
movie_schema = MovieSchema()

#multiple card schema, when many cards need to be retrieved
movies_schema = MovieSchema(many=True)

class ActorSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "f_name", "l_name", "gender", "country", "dob")

#single card schema, when one card needs to be retrieved
actor_schema = ActorSchema()

#multiple card schema, when many cards need to be retrieved
actors_schema = ActorSchema(many=True)

# ROUTING AREA

@app.route("/")
def hello():
  return "Welcome to Ripe Tomatoes API"

@app.route("/movies", methods=["GET"])
def get_movies():
    # get all the cards from the database table
    movie_list = Movie.query.all()
    # Convert the cards from the database into a JSON format and store them in result
    result = movies_schema.dump(movie_list)
    # return the data in JSON format
    return jsonify(result)

@app.route("/actors", methods=["GET"])
def get_actors():
    # get all the cards from the database table
    actor_list = Actor.query.all()
    # Convert the cards from the database into a JSON format and store them in result
    result = actors_schema.dump(actor_list)
    # return the data in JSON format
    return jsonify(result)
