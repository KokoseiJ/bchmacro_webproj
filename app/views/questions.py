from flask import (
    request, Blueprint, redirect, render_template, abort, send_from_directory
)
from sqlalchemy import desc

from app import db
from app.models import Post, Image, User, GhostUser
from app.modules.auth import login_handler, get_id
from app.modules.util import check_image, delete_post

import os
import datetime
from math import ceil


bp = Blueprint(
    name="questions",
    import_name="questions",
    url_prefix="/questions"
)


@bp.route("/", methods=["GET"])
@login_handler
def view_questions(user):
    post_per_page = 9
    post_per_row = 3

    totalpage = ceil(Post.query.filter_by(type=1).count() / post_per_page)

    try:
        page = int(request.args.get("page", "1"))
    except ValueError:
        page = 1

    if page <= 0 or page > totalpage:
        page = 1

    posts = Post.query.filter_by(type=1).order_by(desc(Post.creation_time))\
        .offset(post_per_page*(page-1)).limit(post_per_page).all()

    return render_template(
        "questions/list.html",
        user=user,
        posts=posts,
        page=page,
        totalpage=totalpage,
        perrow=post_per_row
    )


@bp.route("/create", methods=["GET"])
@bp.route("/<id_>/answer", methods=["GET"])
@login_handler
def create_post(user, id_=None):
    if user is None:
        return redirect("/login?return_to=/questions/create")

    return render_template("questions/create.html", user=user)


@bp.route("/create", methods=["POST"])
@bp.route("/<parent_id>/answer", methods=["POST"])
@login_handler
def handle_create_post(user, parent_id=None):
    if parent_id:
        answer = True
    else:
        answer = False

    if user is None:
        return redirect("/login?return_to=/questions/create")

    id_ = get_id(Post)

    file = request.files.get("image")
    if file is not None and file.filename:
        if file.content_length > 100 * 1024 ** 3:
            abort(400)

        ext = check_image(file)
        if not ext:
            abort(400)

        image_id = get_id(Image)

        filename = f"{image_id}.{ext}"

        from flask import current_app
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        image = Image(
            id=image_id,
            author=user.id,
            filename=filename,
            parent_post=id_
        )
    else:
        image = None
        image_id = None

    title = request.form.get("title")
    body = request.form.get("body")

    post = Post(
        id=id_,
        type=1 if answer is False else 2,
        creation_time=datetime.datetime.now(),
        image=image_id,
        title=title,
        author=user.id,
        content=body,
        parent_post=parent_id
    )

    db.session.add(post)

    if image is not None:
        db.session.add(image)

    db.session.commit()

    return redirect(f"/questions/{parent_id if answer else id_}")


@bp.route("/<id_>/", methods=["GET"])
@login_handler
def view_question(id_, user):
    post = Post.query.get(id_)

    if post is None:
        abort(404)

    if post.type == 2:
        return redirect(f"../{post.parent_post}")

    author = User.query.get(post.author)

    if author is None:
        author = GhostUser("삭제된 사용자")

    replies = Post.query.filter_by(parent_post=id_).all()

    return render_template(
        "questions/view.html",
        user=user,
        author=author,
        post=post,
        replies=replies
    )


@bp.route("/<id_>/delete", methods=["GET"])
@login_handler
def delete_question(id_, user):
    if user is None:
        abort(403)

    post = Post.query.get(id_)

    if post is None:
        abort(404)

    if user.account_type == 0 and not user.id == post.author:
        abort(403)

    delete_post(post)

    db.session.commit()

    return redirect("/../../")


@bp.route("/<id_>/image", methods=["GET"])
def redirect_image(id_):
    post = Post.query.get(id_)

    if post is None:
        abort(404)

    if post.image is None:
        return redirect("/static/noimage.png")

    image = Image.query.get(post.image)
    
    if image is None:
        return redirect("/static/noimage.png")

    return redirect(f"/questions/{id_}/image/{image.filename}")


@bp.route("/<id_>/image/<filename>", methods=["GET"])
def get_image(id_, filename):
    post = Post.query.get(id_)

    if post is None or post.image is None:
        abort(404)

    image = Image.query.get(post.image)

    if image is None:
        abort(404)
    if filename != image.filename:
        abort(401)

    from flask import current_app

    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        filename
    )
