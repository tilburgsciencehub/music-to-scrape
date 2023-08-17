from flask import render_template, Blueprint

about_bp = Blueprint('about', __name__)

# route for artist
@about_bp.route('/about')
def about():

    # render template
    return render_template('about.html', head='partials/head.html', loading='partials/loading_empty.html', header='partials/header.html', footer='partials/footer.html')
