from flask import render_template, Blueprint

article_single_bp = Blueprint('article_single', __name__)

# route for artist
@article_single_bp.route('/article_single')
def article_single():

    # render template
    return render_template('article_single.html', head='partials/head.html', loading='partials/loading_empty.html', header='partials/header.html', footer='partials/footer.html')
