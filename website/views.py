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

@views.route('/create-comments/<post_id>', methods = ['GET', 'POST'])
def fetch_comments(post_id):
    from .models import Comments, Posts
    from website import db

    if request.method == 'POST':
        comment_data = request.form.get('comment')
        comment_to_add = Comments(text = comment_data, author = current_user.id, post_id = post_id)
        post = Posts.query.filter(Posts.id == post_id).first()
        print(post)
        post.comments.append(comment_to_add)
        db.session.add(comment_to_add)

        db.session.commit()
        
        flash('comment successfully created', category='success')
    return redirect(url_for('views.home'))


@views.route('/delete-comment/<comment_id>')
def delete_comment(comment_id):
    from website.models import Comments
    from website import db

    comment_to_delete = Comments.query.filter(Comments.id == comment_id).first()

    db.session.delete(comment_to_delete)
    db.session.commit()

    return redirect(url_for('views.home'))

@views.route('like/<post_id>', methods = ['GET'])
def like(post_id):
    from website.models import Posts, Like
    from website import db

    post = Posts.query.filter(Posts.id == post_id)

    like = Like.query.filter(Like.author == current_user.id).first()

    if like:
        print('like already there')
        db.session.delete(like)
        db.session.commit()
    else:
        print('like not there')
        new_like = Like(author = current_user.id, post = post_id)
        db.session.add(new_like)
        current_user.likes.append(new_like)
        db.session.commit()

    return redirect(url_for('views.home'))