### LIBRARIES ###
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc, and_, extract
from sqlalchemy.sql import text
import os
from datetime import datetime, timedelta
from math import ceil
from urllib.parse import urlparse, urlunparse, parse_qsl

# BASIC SETTINGS
# initialize Flask App & Database
app = Flask(__name__)

# get absolute path to Flask app file
app_dir = os.path.abspath(os.path.dirname(__file__))

# construct path to database file
db_path = os.path.join(app_dir, 'apistoscrape.db')

# set database URI in Flask app configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db = SQLAlchemy(app)

### CLASSES FOR TABLES ###

# listening table


class listening(db.Model):
    user = db.Column(db.String)
    date = db.Column(db.Date)
    timestamp = db.Column(db.String)
    artist_id = db.Column(db.String, db.ForeignKey('artists.ArtistID'))
    song_id = db.Column(db.String, db.ForeignKey('songs.SongID'))
    unique_id = db.Column(db.String, primary_key=True)

    artist = db.relationship('artists', backref='listenings')
    song = db.relationship('songs', backref='listenings')

# artists table


class artists(db.Model):
    ArtistID = db.Column(db.String, primary_key=True)
    ArtistName = db.Column(db.String)
    ArtistLocation = db.Column(db.String)
    featured = db.Column(db.String)

# users table


class users(db.Model):
    username = db.Column(db.String, primary_key=True)
    age = db.Column(db.Integer)
    country = db.Column(db.String)
    description = db.Column(db.String)

# songs table


class songs(db.Model):
    ArtistID = db.Column(db.String)
    ArtistName = db.Column(db.String)
    SongID = db.Column(db.String, primary_key=True)
    ArtistID = db.Column(db.Integer)
    Danceability = db.Column(db.Float)
    Duration = db.Column(db.Numeric)
    KeySignature = db.Column(db.Integer)
    Tempo = db.Column(db.Numeric)
    TimeSignature = db.Column(db.Integer)
    Title = db.Column(db.String)
    Year = db.Column(db.Integer)

### ROUTES ###

# route for home
@app.route('/')
def index():

    # recent tracks query
    subquery = db.session.query(
        listening.song_id,
        listening.timestamp
    ).order_by(listening.timestamp.desc()).limit(10).subquery()

    recent_tracks = db.session.query(
        subquery.c.timestamp,
        songs.ArtistName,
        songs.Title,
        songs.SongID
    ).join(songs, subquery.c.song_id == songs.SongID)

    # top 15
    top_songs = db.session.query(listening.song_id, songs.Title, songs.ArtistName, songs.ArtistID,
                                 func.count(listening.song_id),
                                 func.row_number().over(order_by=func.count(listening.song_id).desc()).label('rank'))\
        .join(songs, listening.song_id == songs.SongID)\
        .group_by(listening.song_id)\
        .order_by(func.count(listening.song_id).desc())\
        .limit(15)

    # featured artists
    featured_artists = artists.query.filter_by(
        featured='1').order_by(func.random()).limit(8).all()

    # recent users
    recent_users = db.session.query(
        listening.user,
        func.max(listening.timestamp).label("max_timestamp"),
        songs.ArtistName,
        songs.Title
    ).join(listening.song).group_by(listening.user).order_by(desc("max_timestamp")).limit(6)

    # render template
    return render_template('index.html', head='partials/head.html', header='partials/header.html', footer='partials/footer.html', tracks=recent_tracks, top_songs=top_songs, featured_artists=featured_artists, recent_users=recent_users)

# route for artist


@app.route('/artist')
def artist_page():

    # get artist id parameter
    artist_id = request.args.get('artist-id')

    # get artist info
    artist_info = artists.query.filter_by(ArtistID=artist_id).first()

    # count number of songs
    num_songs = songs.query.filter_by(ArtistID=artist_id).count()

    # top 10 songs for artist
    top_songs = db.session.query(
        db.func.row_number().over(order_by=db.func.count(
            listening.song_id).desc()).label('rank'),
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

    # render template
    return render_template('artist_page.html', head='partials/head.html', header='partials/header.html', footer='partials/footer.html', artist_id=artist_id, artist_info=artist_info, num_songs=num_songs, top_songs=top_songs)

# route for user


@app.route('/user')
def user_page():

    # get username
    username = request.args.get('username')

    # get artist info
    user_info = users.query.filter_by(username=username).first()

    # get the weeknumber and year
    week = request.args.get('week')
    year_number = request.args.get('year')

    if week:
        if int(week) < 0:
            # Parse the current URL
            parsed_url = urlparse(request.url)
            query_params = dict(parse_qsl(parsed_url.query))

            # Modify the 'week' argument
            query_params['week'] = '0'

            # Construct the new URL with the modified query parameters
            modified_url = urlunparse(parsed_url._replace(query='&'.join(
                f"{key}={value}" for key, value in query_params.items())))

            # Redirect to the new URL
            return redirect(modified_url)

    # current week
    current_date = datetime.now()
    current_week = current_date.isocalendar()[1]

    # if statement to check if week & year have been set
    if week:
        if int(week) >= 0:
            week_number = int(week)

        else:
            week_number = 0

    else:
        week_number = current_week

    if year_number:
        year = year_number

    else:
        year = datetime.now().year

    # previous and next week
    next_week = int(week_number) + 1
    prev_week = int(week_number) - 1
    curr_week = int(week_number)
    week_plus_one = curr_week + 1
    week_min_one = curr_week + -1

    # create navigation dict
    nav_dict = {'next_week': next_week, 'prev_week': prev_week, 'curr_week': curr_week,
                'week_plus_one': week_plus_one, 'week_min_one': week_min_one}

    # get the start and end date of the week
    start_date = datetime.strptime(f"{year}-W{week_number}-1", "%Y-W%W-%w")
    end_date = start_date + timedelta(days=6)

    # top 10 songs
    top_songs = db.session.query(songs.Title, songs.ArtistName, listening.timestamp).\
        join(songs, listening.song_id == songs.SongID).\
        filter(listening.user == username).\
        filter(listening.date >= start_date.date(), listening.date <= end_date.date()).\
        group_by(listening.timestamp).\
        order_by(listening.timestamp).\
        limit(10).all()

    # Create a list to store the formatted data
    formatted_songs = []

    # Loop through each record and format the timestamp
    for song in top_songs:
        title, artist_name, timestamp = song
        datetime_obj = datetime.fromtimestamp(float(timestamp))
        formatted_date = datetime_obj.strftime('%Y-%m-%d')
        formatted_time = datetime_obj.strftime('%H:%M:%S')
        formatted_songs.append(
            (title, artist_name, formatted_date, formatted_time))

    # render template
    return render_template('user_page.html', head='partials/head.html', header='partials/header.html', footer='partials/footer.html', user_info=user_info, top_songs=formatted_songs, nav_dict=nav_dict, start_date=start_date.date(), end_date=end_date.date(), current_week=current_week)

# route for search


@app.route('/search')
def search():
    query = request.args.get('query')
    results = []
    page = request.args.get('page', type=int, default=1)

    if query:
        # search for username in users table
        users_results = users.query.filter(
            users.username.ilike(f'%{query}%')).all()
        results.extend(users_results)

        # search for title in songs table
        songs_results = songs.query.filter(
            songs.Title.ilike(f'%{query}%')).all()
        results.extend(songs_results)

        # search for ArtistName in artists table
        artists_results = artists.query.filter(
            artists.ArtistName.ilike(f'%{query}%')).all()
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
    prev_url = url_for('search', query=query,
                       page=page-1) if page > 1 else None
    next_url = url_for('search', query=query, page=page +
                       1) if page < total_pages else None

    # number of results on a page
    start_result = ((page - 1) * 10) + 1

    if (start_result + 9) > total_results:
        end_result = total_results

    else:
        end_result = start_result + 9

    # Render the results for the current page
    return render_template('search_results.html', head='partials/head.html', header='partials/header.html', footer='partials/footer.html', total_results=total_results, max_pages=max_pages, results=current_page_results, page=page, query=query, total_pages=total_pages, prev_url=prev_url, next_url=next_url, start_result=start_result, end_result=end_result)

# route for privacy & terms


@app.route('/privacy_terms')
def privacy_terms():

    # render template
    return render_template('privacy_terms.html', head='partials/head.html', header='partials/header.html', footer='partials/footer.html')



@app.route('/about')
def about():

    # render template
    return render_template('about.html', head='partials/head.html', header='partials/header.html', footer='partials/footer.html')
# route for article


@app.route('/article')
def article_single():

    # render template
    return render_template('article_single.html', head='partials/head.html', header='partials/header.html', footer='partials/footer.html')

# route for song page


@app.route('/song')
def song():

    # get artist id parameter
    song_id = request.args.get('song-id')

    # get artist info
    song_info = songs.query.filter_by(SongID=song_id).first()

    # num plays
    num_plays = listening.query.filter_by(song_id=song_id).count()

    # top listeners
    top_listeners = db.session.query(listening.user, func.count(listening.unique_id).label("play_count")) \
        .filter(listening.song_id == song_id) \
        .group_by(listening.user) \
        .order_by(desc("play_count")) \
        .limit(5) \
        .all()

    #age groups
    age_10_29_count = db.session.query(func.count(func.distinct(listening.user))) \
    .join(users, listening.user == users.username) \
    .filter(listening.song_id == song_id) \
    .filter(users.age < 29) \
    .scalar()

    age_30_49_count = db.session.query(func.count(func.distinct(listening.user))) \
        .join(users, listening.user == users.username) \
        .filter(listening.song_id == song_id) \
        .filter(users.age.between(30, 50)) \
        .scalar()

    age_above_49_count = db.session.query(func.count(func.distinct(listening.user))) \
        .join(users, listening.user == users.username) \
        .filter(listening.song_id == song_id) \
        .filter(users.age > 50) \
        .scalar()
    
    age_groups = {'group1':age_10_29_count,'group2':age_30_49_count,'group3':age_above_49_count}

    #plays per month
    current_year = datetime.today().year

    plays_per_month = db.session.query(
            func.extract('month', listening.date).label('month'),
            func.count().label('plays')
        ).join(users, listening.user == users.username
        ).filter(listening.song_id == song_id
        ).filter(extract('year', listening.date) == current_year
        ).group_by(func.extract('month', listening.date)
        ).order_by(func.extract('month', listening.date)
        ).all()
    
    # Plays per Country
    plays_per_country = db.session.query(
        users.country,
        func.count().label('plays')
    ).join(listening, listening.user == users.username
    ).filter(listening.song_id == song_id
    ).group_by(users.country
    ).all()

    # Define a list of month names
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']

    # Map month number to month name
    plays_per_month = [(month_names[int(month) - 1], plays) for month, plays in plays_per_month]
    
    #Unique listeners per country
    unique_listeners_per_country = db.session.query(
        users.country,
        func.count(func.distinct(listening.user)).label('unique_listeners')
    ).join(listening, listening.user == users.username
    ).filter(listening.song_id == song_id
    ).group_by(users.country
    ).all()


    # render template
    return render_template('song_page.html', head='partials/head.html', header='partials/header.html', footer='partials/footer.html', song_info=song_info, num_plays=num_plays, top_listeners=top_listeners, age_groups=age_groups, plays_per_month=plays_per_month, plays_per_country=plays_per_country, unique_listeners_per_country=unique_listeners_per_country)


# Add a static route for CSS


@app.route('/static/css/<path:path>')
def static_css(path):
    return app.send_static_file('css/' + path)


if __name__ == '__main__':
    app.run(debug=True)
