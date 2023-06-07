from flask import render_template, Blueprint

privacy_terms_bp = Blueprint('privacy_terms', __name__)

# route for artist
@privacy_terms_bp.route('/privacy_terms')
def privacy_terms():

    # render template
    return render_template('privacy_terms.html', head='partials/head.html', loading='partials/loading_empty.html', header='partials/header.html', footer='partials/footer.html')
