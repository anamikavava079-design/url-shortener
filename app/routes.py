from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import URL
import random, string

main = Blueprint('main', __name__)

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@main.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        original = request.form['url']
        code = generate_code()
        new_url = URL(original_url=original, short_code=code)
        db.session.add(new_url)
        db.session.commit()
        short_url = request.host_url + code
    return render_template('index.html', short_url=short_url)

@main.route('/<code>')
def redirect_url(code):
    url = URL.query.filter_by(short_code=code).first_or_404()
    url.click_count += 1
    db.session.commit()
    return redirect(url.original_url)

@main.route('/analytics')
def analytics():
    urls = URL.query.order_by(URL.click_count.desc()).all()
    return render_template('analytics.html', urls=urls)
