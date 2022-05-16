from flask import render_template, redirect, url_for, flash, request, jsonify, abort
from . import main
from ..requests import randomquote
from sqlalchemy import desc
from .forms import CommentForm, BlogForm, UpdateProfile
from ..models import User, Blog, Photos, Comment, Subscriptions, Likes, Dislikes
from flask_login import login_required, current_user
import os
from app import photos
from .. import db


@main.route('/')
def index():
    randomized_quote = randomquote()
    title = 'Home'
    commentform = CommentForm()
    blogs = all_blogs(Blog.query.all())
    recent_blogs = all_blogs(Blog.query.order_by(desc('blog_created'))[:4])
    return render_template('index.html', quotes=randomized_quote, title=title, commentform=commentform, blogs=blogs,
                           recent_blogs=recent_blogs)


def all_blogs(blogs):
    for blog in blogs:
        blog.user = User.query.filter_by(id=blog.author_id).first()
        for comment in blog.comments:
            comment.user = User.query.filter_by(id=comment.user_id).first()
    return blogs


@login_required
@main.route('/<int:user_id>/blogs')
def blogs(user_id):
    commentform = CommentForm()
    blogs = Blog.query.filter_by(author_id=user_id).all()
    return render_template('blogs.html', blogs=blogs, commentform=commentform)


# about
def about():
    return render_template('about.html')


# new blog view
@login_required
@main.route('/blog/<int:user_id>/new', methods=['GET', 'POST'])
def newblog(user_id):
    blogform = BlogForm()
    title = "New Blog"
    if blogform.validate_on_submit():
        title = blogform.title.data
        body = blogform.blog.data
        blog = Blog(author_id=user_id, title=title, blog=body)
        blog.save()
        return redirect(url_for('main.index', user_id=user_id))
    return render_template('forms/newblog.html', title=title, blogform=blogform)


@main.route('/comment/<int:blog_id>/add', methods=['POST'])
@login_required
def add_comment(blog_id):
    commentform = CommentForm()
    title = "Comment"
    if commentform.validate_on_submit():
        comment = commentform.commentbody.data
        new_comment = Comment(comment=comment, user_id=current_user.id, blog_id=blog_id)
        new_comment.save()
        user = User.query.filter_by(id=current_user.id).first()
        comment = {'comment': commentform.commentbody.data, 'user': user.username,
                   'blog': blog_id}
        flash("New comment added success successfully", 'success')
        return jsonify(comment)
        # return redirect(url_for('main.blogs', user_id=current_user.id))
    return render_template('index.html', title=title)


@main.route('/<int:user_id>/profile', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    if 'photo' in request.files:
        if user.profile_pic_path:
            user_photo = f'/{user.profile_pic_path.split("/")[1]}'
            path = os.path.abspath(os.environ.get('UPLOADED_PHOTOS_DEST') + user_photo)
            if os.path.exists(path):
                os.remove(path)

        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        user.save()
        return redirect(url_for('main.profile', user_id=user_id))
    return render_template('profile/profile.html', user=user)


@main.route('/user/<int:user_id>/update', methods=['GET', 'POST'])
@login_required
def update_profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)
    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile', user_id=user.id))
    return render_template('profile/updateprofile.html', form=form)


@main.route('/like/<int:id>', methods=['POST'])
@login_required
def like(id):
    blog = Blog.query.get(id)
    new_like = Likes(blog = blog, upvote = 1, user_id = current_user.id)
    new_like.save()
    return redirect(url_for('main.index'))

@main.route('/like/<int:id>', methods=['POST'])
@login_required
def dislike(id):
    blog = Blog.query.get(id)
    new_dislike = Dislikes(blog = blog, downvote = 1, user_id = current_user.id)
    new_dislike.save()
    return redirect(url_for('main.index'))


# @main.route('/blog/<string:vote>/<int:pitch_id>', methods=['POST'])
# def toggleLikes(like, blog_id):
#     if like == 'like':
#         new_like = Likes(user_id=current_user.id, blog_id=blog_id)
#         new_like.toggleLike()
#
#     elif like == 'dislike':
#         new_dislike = Likes(user_id=current_user.id, blog_id=blog_id)
#         new_dislike.toggleLike()
#     likes = Likes.query.filter_by(blog_id=blog_id).count()
#     dislikes = Dislikes.query.filter_by(blog_id=blog_id).count()
#
#     return jsonify(likes, dislikes)
