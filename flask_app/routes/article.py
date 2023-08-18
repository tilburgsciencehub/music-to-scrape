from flask import render_template, Blueprint

article_tutorial_scraping_bp = Blueprint('article_tutorial_scraping', __name__)

# route for article
@article_tutorial_scraping_bp.route('/tutorial_scraping')
def article_tutorial_scraping():

    # render template
    return render_template('article_tutorial_scraping.html', head='partials/head.html', loading='partials/loading_empty.html', header='partials/header.html', footer='partials/footer.html')
