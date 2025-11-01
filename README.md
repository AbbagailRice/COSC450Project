# COSC450Project
IMDB Movie Database Project
Database Schema

Schema:
Main Tables: Movies

Dimension Tables: People, Genres, Certificates, Roles

Linking Tables: MovieGenres and MoviePeople to manage the many-to-many relationships (e.g., a movie has multiple genres, a person can be in multiple movies).

How to Use

You need a running MySQL server Xampp or mysql server

Create the Database Schema:

Open imdb_schema.sql in your MySQL client (I used MySQL Workbench).
Execute the script (with lightning bolt in Workbench). This will create the movie_db database and all the empty tables.

Populate the Database:

Open insert_data.sql in your MySQL client.
Execute the script. This will run all the INSERT statements and populate the tables with all 1,000 movies and their related data.

Using the Flask site and connecting to database:
You need to install SQLAlchemy and PyMySQL, so run
pip install Flask-SQLAlchemy
pip install PyMySQL
and then change the username and password in the ['SQLALCHEMY_DATABASE_URI'] line to match your SQL database.
To test that it works, remove the homepage function, and refresh the site. If it works, it will say "It works" on the page.