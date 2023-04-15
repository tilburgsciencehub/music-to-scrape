### LIBRARIES ###
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.sql import text
import os
from datetime import datetime, timedelta
from math import ceil

### BASIC SETTINGS
#initialize Flask App & Database
app = Flask(__name__)

# get absolute path to Flask app file
app_dir = os.path.abspath(os.path.dirname(__file__))

# construct path to database file
db_path = os.path.join(app_dir, 'apistoscrape.db')

# set database URI in Flask app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db = SQLAlchemy(app)

### CLASSES FOR TABLES ###

#listening table
class listening(db.Model):
    user = db.Column(db.String(10))
    date = db.Column(db.Date)
    timestamp = db.Column(db.String(16))
    artist_id = db.Column(db.String(18), db.ForeignKey('artists.ArtistID'))
    song_id = db.Column(db.String(18), db.ForeignKey('songs.SongID'))
    unique_id = db.Column(db.String(52), primary_key=True)

    artist = db.relationship('artists', backref='listenings')
    song = db.relationship('songs', backref='listenings')

#artists table
class artists(db.Model):
    ArtistID = db.Column(db.String(18), primary_key=True)
    ArtistName = db.Column(db.String(400))
    ArtistLocation = db.Column(db.String(200))
    featured = db.Column(db.String(5))

#users table
class users(db.Model):
    username = db.Column(db.String(18), primary_key=True)
    age = db.Column(db.Integer)
    country = db.Column(db.String(2))
    description = db.Column(db.String(500))

#songs table
class songs(db.Model):
    ArtistID = db.Column(db.String(20))
    ArtistName = db.Column(db.String(400))
    SongID = db.Column(db.String(20), primary_key=True)
    ArtistID = db.Column(db.Integer)
    Danceability = db.Column(db.Numeric(1,0))
    Duration = db.Column(db.Numeric(15,5))
    KeySignature = db.Column(db.Integer)
    Tempo = db.Column(db.Numeric(20,3))
    TimeSignature = db.Column(db.Integer)
    Title = db.Column(db.String(400))
    Year = db.Column(db.Integer)

### ROUTES ### 

#route for home
@app.route('/')
def index():

    #recent tracks query
    recent_tracks = db.session.query(listening.timestamp, songs.ArtistName, songs.Title)\
                .join(songs, listening.song_id == songs.SongID)\
                .order_by(listening.timestamp.desc())\
                .limit(10)\
                .all()
    
    #weekly top 15
    top_songs = db.session.query(listening.song_id, songs.Title, songs.ArtistName, 
                    func.count(listening.song_id), 
                    func.row_number().over(order_by=func.count(listening.song_id).desc()).label('rank'))\
            .join(songs, listening.song_id == songs.SongID)\
            .group_by(listening.song_id)\
            .order_by(func.count(listening.song_id).desc())\
            .limit(15)\
            .all()
    
    #featured artists
    featured_artists = artists.query.filter_by(featured='TRUE').order_by(func.random()).limit(8).all()

    #recent users
    recent_users = db.session.query(listening.timestamp, listening.user, songs.ArtistName, songs.Title)\
                .join(songs, listening.song_id == songs.SongID)\
                .group_by(listening.user)\
                .order_by(listening.timestamp.desc())\
                .limit(6)\
                .all()
    
    #render template
    return render_template('index.html', tracks = recent_tracks, top_songs = top_songs, featured_artists = featured_artists, recent_users = recent_users)

#route for artist
@app.route('/artist')
def artist_page():

    #get artist id parameter
    artist_id = request.args.get('artist-id')

    #get artist info
    artist_info = artists.query.filter_by(ArtistID=artist_id).first()

    #count number of songs
    num_songs = songs.query.filter_by(ArtistID=artist_id).count()

    #top 10 songs for artist
    top_songs = db.session.query(
                    db.func.row_number().over(order_by=db.func.count(listening.song_id).desc()).label('rank'),
                    listening.song_id,
                    db.func.count(listening.song_id).label('count'),
                    songs.Title,
                    songs.ArtistName
                ).\
                join(songs, listening.song_id == songs.SongID).\
                filter(listening.artist_id == artist_id).\
                group_by(listening.song_id).\
                order_by(db.func.count(listening.song_id).desc()).\
                limit(10).all()

    #render template
    return render_template('artist_page.html', artist_id = artist_id, artist_info = artist_info, num_songs = num_songs, top_songs = top_songs)

#route for user
@app.route('/user')
def user_page():

    #get username
    username = request.args.get('username')

    #get artist info
    user_info = users.query.filter_by(username=username).first()

    #get the weeknumber and year
    week = request.args.get('week')
    year_number = request.args.get('year')

    #if statement to check if week & year have been set
    if week:
        week_number = week

    else:
        week_number = 1

    if year_number:
        year = year_number
    
    else:
        year = 2023

    #previous and next week
    next_week = int(week_number) + 1
    prev_week = int(week_number) - 1
    curr_week = int(week_number)
    week_plus_one = curr_week + 1
    week_min_one = curr_week + -1

    #create navigation dict
    nav_dict = {'next_week' : next_week, 'prev_week' : prev_week, 'curr_week' : curr_week, 'week_plus_one' : week_plus_one, 'week_min_one' : week_min_one}

    #get the start and end date of the week
    start_date = datetime.strptime(f"{year}-W{week_number}-1", "%Y-W%W-%w")
    end_date = start_date + timedelta(days=6)

    #top 10 songs
    top_songs = db.session.query(
                    db.func.row_number().over(order_by=db.func.count(listening.song_id).desc()).label('rank'),
                    listening.song_id,
                    db.func.count(listening.song_id).label('count'),
                    songs.Title,
                    songs.ArtistName
                ).\
                join(songs, listening.song_id == songs.SongID).\
                filter(listening.user == username).\
                filter(listening.date >= start_date.date(), listening.date <= end_date.date()).\
                group_by(listening.song_id).\
                order_by(db.func.count(listening.song_id).desc()).\
                limit(10).all()

    #render template
    return render_template('user_page.html', user_info = user_info, top_songs = top_songs, nav_dict = nav_dict)

#route for search
@app.route('/search')
def search():
    query = request.args.get('query')
    results = []
    page = request.args.get('page', type=int, default=1)

    if query:
        # search for username in users table
        users_results = users.query.filter(users.username.ilike(f'%{query}%')).all()
        results.extend(users_results)
        
        # search for title in songs table
        songs_results = songs.query.filter(songs.Title.ilike(f'%{query}%')).all()
        results.extend(songs_results)
        
        # search for ArtistName in artists table
        artists_results = artists.query.filter(artists.ArtistName.ilike(f'%{query}%')).all()
        results.extend(artists_results)

    # Total Results
    total_results = len(results)

    # Set the number of results per page
    RESULTS_PER_PAGE = 10

    # Set the max of pages
    max_pages = 10

    # Calculate the total number of pages
    # Calculate the total number of pages
    total_pages = (len(results) + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE

    # Calculate the start and end indices for the current page
    start_index = (page - 1) * RESULTS_PER_PAGE
    end_index = start_index + RESULTS_PER_PAGE

    # Get the subset of results for the current page
    current_page_results = results[start_index:end_index]

    # Generate URLs for the previous and next pages
    prev_url = url_for('search', query=query, page=page-1) if page > 1 else None
    next_url = url_for('search', query=query, page=page+1) if page < total_pages else None

    # Render the results for the current page
    return render_template('search_results.html',total_results=total_results, max_pages=max_pages, results=current_page_results, page=page, query=query, total_pages=total_pages, prev_url = prev_url, next_url = next_url)

# Add a static route for CSS
@app.route('/static/css/<path:path>')
def static_css(path):
    return app.send_static_file('css/' + path)

if __name__ == '__main__':
    app.run(debug=True)
