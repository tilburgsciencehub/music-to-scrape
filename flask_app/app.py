### LIBRARIES ###
from flask import Flask
from database import init_app
from routes.artist import artist_bp
from routes.user import user_bp
from routes.search import search_bp
from routes.song import song_bp
from routes.privacy_terms import privacy_terms_bp
from routes.article import article_single_bp
from routes.home import home_bp

# BASIC SETTINGS
# initialize Flask App & Database
app = Flask(__name__)

# Initialize the database with the Flask app
init_app(app)

# route for home
app.register_blueprint(home_bp)

# route for artist
app.register_blueprint(artist_bp)

# route for user
app.register_blueprint(user_bp)

# route for search
app.register_blueprint(search_bp)

# route for privacy & terms
app.register_blueprint(privacy_terms_bp)

# route for article
app.register_blueprint(article_single_bp)

# route for song page
app.register_blueprint(song_bp)

# Add a static route for CSS
@app.route('/static/css/<path:path>')
def static_css(path):
    return app.send_static_file('css/' + path)


if __name__ == '__main__':
    app.run(debug=True)
