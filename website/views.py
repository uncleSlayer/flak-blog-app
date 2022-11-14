from flask import Blueprint, render_template
# from flask_login import login_required
from .auth import login_required

views = Blueprint('views', __name__)

@login_required
@views.route('/')
def home():
    return render_template('home.html', name = 'Siddhant')