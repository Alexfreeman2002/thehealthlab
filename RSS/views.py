from flask import render_template
import feedparser
from flask import Blueprint

news_blueprint = Blueprint('news', __name__, template_folder='templates/features')


@news_blueprint.route('/features/news', methods=['get'])
def news():
    feed = feedparser.parse('https://www.england.nhs.uk/feed/')
    articles = feed.entries[:10]
    return render_template('features/news.html', articles=articles)


