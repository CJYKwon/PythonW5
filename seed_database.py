import os
import json
from random import choice, randint
from datetime import datetime

from flask import app

import crud
import model
import server

os.system("dropdb -U postgres ratings")
os.system("createdb -U postgres ratings")

model.connect_to_db(server.app)

with server.app.app_context():
    model.db.create_all()

    with open("data/movies.json") as f:
        movie_data = json.loads(f.read())

        movies_in_db = []

        for movie in movie_data:
            title = movie["title"]
            overview = movie["overview"]
            poster_path = movie["poster_path"]

            release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

            new_movie = crud.create_movie(title, overview, release_date, poster_path)

            movies_in_db.append(new_movie)

        model.db.session.add_all(movies_in_db)
        model.db.session.commit()

        for n in range(10):
            email = f"user{n}@test.com"
            password = "test"

            new_user = crud.create_user(email, password)
            model.db.session.add(new_user)

            for n in range(10):
                random_movie = choice(movies_in_db)
                score = randint(1, 5)

                new_rating = crud.create_rating(new_user, random_movie, score)
                model.db.session.add(new_rating)

        model.db.session.commit()