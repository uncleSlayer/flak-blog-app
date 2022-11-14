from flask import Blueprint, render_template, request, flash, redirect, url_for
from .auth import login_required
from flask_login import current_user

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    from .models import Posts
    all_posts = Posts.query.all()
    print(all_posts)
    return render_template('home.html', current_user = current_user, all_posts=all_posts)

@views.route('/create-post', methods = ['GET', 'POST'])
def create_post():
    from .models import Posts
    from . import db
    if request.method == 'POST':
        form_data = request.form
        post_text_input = form_data.get('post')
        post = Posts(text = post_text_input, author = current_user.id)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('views.home'))

    return render_template('create_post.html')

@views.route('/delete-post/<id>')
def delete_post(id):
    from .models import Posts
    from . import db
    # flash(id)
    post_to_delete = Posts.query.filter(Posts.id == id).first()
    # print(post_to_delete, 'hello')

    if not post_to_delete:
        flash('this is not a valid request', category='error')

    elif current_user.id != post_to_delete.author:
        flash('you are not allowed to delete the post', category='error')

    else:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash('post deleted', category='success')
    return redirect(url_for('views.home'))