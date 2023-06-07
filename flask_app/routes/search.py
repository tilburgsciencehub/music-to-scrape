from flask import render_template, request, Blueprint, url_for
from database import init_app, db
from models import listening, artists, songs, users
from datetime import datetime, timedelta
from urllib.parse import urlparse, urlunparse, parse_qsl

search_bp = Blueprint('search', __name__)

# route for artist
@search_bp.route('/search')
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
    prev_url = url_for('search.search', query=query,
                       page=page-1) if page > 1 else None
    next_url = url_for('search.search', query=query, page=page +
                       1) if page < total_pages else None

    # number of results on a page
    start_result = ((page - 1) * 10) + 1

    if (start_result + 9) > total_results:
        end_result = total_results

    else:
        end_result = start_result + 9

    # Render the results for the current page
    return render_template('search_results.html', head='partials/head.html', loading='partials/loading_empty.html', header='partials/header.html', footer='partials/footer.html', total_results=total_results, max_pages=max_pages, results=current_page_results, page=page, query=query, total_pages=total_pages, prev_url=prev_url, next_url=next_url, start_result=start_result, end_result=end_result)
