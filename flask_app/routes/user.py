from flask import render_template, request, Blueprint, redirect
from database import init_app, db
from models import listening, artists, songs, users
from datetime import datetime, timedelta
from urllib.parse import urlparse, urlunparse, parse_qsl

user_bp = Blueprint('user', __name__)

# route for artist
@user_bp.route('/user')
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
        order_by(listening.timestamp.desc()).\
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
    return render_template('user_page.html', head='partials/head.html', loading='partials/loading_empty.html', header='partials/header.html', footer='partials/footer.html', user_info=user_info, top_songs=formatted_songs, nav_dict=nav_dict, start_date=start_date.date(), end_date=end_date.date(), current_week=current_week)
