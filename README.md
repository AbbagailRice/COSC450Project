# COSC450Project
IMDB Movie Database Project
Database Schema

Schema:
Main Tables: Movies

Dimension Tables: People, Genres, Certificates, Roles

Linking Tables: MovieGenres and MoviePeople to manage the many-to-many relationships (e.g., a movie has multiple genres, a person can be in multiple movies).

How to Use

You need a running MySQL server Xamp or mysql server

Create the Database Schema:

Open imdb_schema.sql in your MySQL client (I used MySQL Workbench).
Execute the script (with lightning bolt in Workbench). This will create the movie_db database and all the empty tables.

Populate the Database:

Open insert_data.sql in your MySQL client.
Execute the script. This will run all the INSERT statements and populate the tables with all 1,000 movies and their related data.
