from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

# Flask will automatically look for 'templates' and 'static' folders
app = Flask(__name__)
#change root and sparrow to match your database username and password
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:sparrow@localhost/movie_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db= SQLAlchemy(app)

@app.route('/')
def homepage():
    """Serves the main homepage."""
    # This tells Flask to find 'index.html' in the 'templates' folder
    return render_template('index.html')

#function that tests to make sure the database connection works (it displays "It works" if you remove the homepage function)
def testdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


if __name__ == '__main__':
    # You'll need to run: pip install Flask
    app.run(debug=True)
