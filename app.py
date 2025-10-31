from flask import Flask, render_template

# Flask will automatically look for 'templates' and 'static' folders
app = Flask(__name__)

@app.route('/')
def homepage():
    """Serves the main homepage."""
    # This tells Flask to find 'index.html' in the 'templates' folder
    return render_template('index.html')

if __name__ == '__main__':
    # You'll need to run: pip install Flask
    app.run(debug=True)
