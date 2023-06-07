from flask import render_template, request, Blueprint
from database import init_app, db
from models import listening, songs, users
from datetime import datetime
from urllib.parse import urlparse, urlunparse, parse_qsl
from sqlalchemy import func, desc, extract

song_bp = Blueprint('song', __name__)

# route for artist
@song_bp.route('/song')
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
    return render_template('song_page.html', head='partials/head.html', loading='partials/loading_empty.html', header='partials/header.html', footer='partials/footer.html', song_info=song_info, num_plays=num_plays, top_listeners=top_listeners, age_groups=age_groups, plays_per_month=plays_per_month, plays_per_country=plays_per_country, unique_listeners_per_country=unique_listeners_per_country)
