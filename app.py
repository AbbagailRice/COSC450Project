from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)

# DATABASE CONFIGURATION
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sparrow@localhost/movie_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def homepage():
    """
    Handles: Retrieve, Search, and Filter
    """
    try:
        search_query = request.args.get('search', '')
        genre_filter = request.args.get('genre', '')

        # Fetch Genres for Dropdown
        genre_sql = text("SELECT DISTINCT GenreName FROM Genres ORDER BY GenreName")
        genres = db.session.execute(genre_sql).fetchall()

        # Build Dynamic Query
        base_query = """
            SELECT DISTINCT m.MovieID, m.Series_Title AS Title, m.Released_Year AS ReleasedYear, 
                   m.IMDB_Rating, m.RuntimeMinutes AS Runtime, m.Poster_Link AS PosterLink
            FROM Movies m
        """
        
        if genre_filter:
            base_query += """
                JOIN MovieGenres mg ON m.MovieID = mg.MovieID
                JOIN Genres g ON mg.GenreID = g.GenreID
            """
        
        base_query += " WHERE 1=1" 
        params = {}

        if search_query:
            base_query += " AND m.Series_Title LIKE :search"
            params['search'] = f"%{search_query}%"

        if genre_filter:
            base_query += " AND g.GenreName = :genre"
            params['genre'] = genre_filter

        base_query += " ORDER BY m.IMDB_Rating DESC LIMIT 50"

        result = db.session.execute(text(base_query), params)
        movies = result.fetchall()
        
        return render_template('index.html', movies=movies, genres=genres, 
                               current_search=search_query, current_genre=genre_filter)
        
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

# CRUD

@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    """Page to Add a new movie."""
    if request.method == 'POST':
        try:
            # Get data from the form
            title = request.form['title']
            year = request.form['year']
            rating = request.form['rating']
            runtime = request.form['runtime']
            overview = request.form['overview']
            poster = request.form['poster']

            # Insert Query
            moviesql = text("""
                INSERT INTO Movies (Series_Title, Released_Year, IMDB_Rating, RuntimeMinutes, Overview, Poster_Link)
                VALUES (:title, :year, :rating, :runtime, :overview, :poster)
            """)
            
            db.session.execute(moviesql, {
                'title': title, 'year': year, 'rating': rating, 
                'runtime': runtime, 'overview': overview, 'poster': poster
            })

            db.session.commit()

            # Redirect back to home after saving
            return redirect(url_for('homepage'))
        except Exception as e:
            return f"Error adding movie: {str(e)}"
        
    # If GET request, show the form (empty)
    return render_template('form.html', action="Add")

@app.route('/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    """Page to Update an existing movie."""
    if request.method == 'POST':
        try:
            # Get data from form
            title = request.form['title']
            year = request.form['year']
            rating = request.form['rating']
            runtime = request.form['runtime']
            overview = request.form['overview']
            poster = request.form['poster']

            # Update Query
            sql = text("""
                UPDATE Movies 
                SET Series_Title=:title, Released_Year=:year, IMDB_Rating=:rating, 
                    RuntimeMinutes=:runtime, Overview=:overview, Poster_Link=:poster
                WHERE MovieID=:id
            """)
            
            db.session.execute(sql, {
                'title': title, 'year': year, 'rating': rating, 
                'runtime': runtime, 'overview': overview, 'poster': poster, 'id': movie_id
            })
            db.session.commit()
            
            return redirect(url_for('homepage'))
        except Exception as e:
            return f"Error updating movie: {str(e)}"
    
    # Fetch existing movie data to pre-fill form
    sql = text("SELECT * FROM Movies WHERE MovieID = :id")
    result = db.session.execute(sql, {'id': movie_id}).fetchone()
    
    if not result:
        return "Movie not found"

    # Pass 'result' object to template
    return render_template('form.html', action="Edit", movie=result)

@app.route('/delete/<int:movie_id>')
def delete_movie(movie_id):
    """Action to Delete a movie."""
    try:
        # Delete from linking tables first to avoid Foreign Key errors
        db.session.execute(text("DELETE FROM MovieGenres WHERE MovieID = :id"), {'id': movie_id})
        db.session.execute(text("DELETE FROM MoviePeople WHERE MovieID = :id"), {'id': movie_id})
        
        # delete the movie
        db.session.execute(text("DELETE FROM Movies WHERE MovieID = :id"), {'id': movie_id})
        db.session.commit()
        
        return redirect(url_for('homepage'))
    except Exception as e:
        return f"Error deleting movie: {str(e)}"


@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    """Recommendations to be generated by rating, genre, and release year"""
    try:
        # get form values 
        genre = request.form.get('genre', '')
        rating = request.form.get('rating', '')
        year = request.form.get('year', '')

        genre_sql = text("SELECT DISTINCT GenreName FROM Genres ORDER BY GenreName")
        genres = db.session.execute(genre_sql).fetchall()

        base_query = """ SELECT DISTINCT m.MovieID, m.Series_Title AS Title, 
        m.Released_Year AS ReleasedYear, m.IMDB_Rating, m.RuntimeMinutes AS Runtime, 
        m.Poster_Link AS PosterLink, m.Overview FROM Movies m"""

        params = {}

        if genre:
            base_query += """ JOIN MovieGenres mg ON m.MovieID = mg.MovieID 
            JOIN Genres g ON mg.GenreID = g.GenreID"""

        base_query += " WHERE 1=1"

        # apply filters
        if genre:
            base_query += " AND g.GenreName = :genre"
            params['genre'] = genre

        if rating:
            base_query += " AND m.IMDB_Rating >= :rating"
            params['rating'] = float(rating)

        if year:
            base_query += " AND m.Released_Year >= :year"
            params['year'] = int(year)


        base_query += " ORDER BY m.IMDB_Rating DESC LIMIT 50"

        result = db.session.execute(text(base_query), params)
        recommendations = result.fetchall()

        return render_template('recommendations.html', recommendations=recommendations, genres=genres, current_genre=genre, current_rating = rating, current_year = year)
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True)