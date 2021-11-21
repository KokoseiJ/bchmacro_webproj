from app import db


class User(db.Model):
    id = db.Column(
        # Base64url 6바잍
        db.String(8),
        primary_key=True,
        unique=True,
        nullable=False
    )

    creation_time = db.Column(
        db.DateTime,
        unique=False,
        nullable=False
    )

    email = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    nickname = db.Column(
        db.String(15),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(10),
        unique=False,
        nullable=False
    )

    password = db.Column(
        # bcrypt 12단계
        db.String(60),
        unique=False,
        nullable=False
    )

    student_number = db.Column(
        db.Integer,
        unique=False,
        nullable=True
    )

    account_type = db.Column(
        db.Integer,
        unique=False,
        nullable=False
    )


class Post(db.Model):
    id = db.Column(
        # Base64url 9바이트
        db.String(12),
        primary_key=True,
        unique=True,
        nullable=False
    )

    type = db.Column(
        # 1은 질문, 2는 답변, 0은 공지 같은식
        db.Integer,
        unique=False,
        nullable=False
    )

    creation_time = db.Column(
        db.DateTime,
        unique=False,
        nullable=False
    )

    image = db.Column(
        # Placeholder
        db.String(12),
        unique=False,
        nullable=False
    )

    author = db.Column(
        db.String(8),
        unique=False,
        nullable=False
    )

    content = db.Column(
        db.Text,
        unique=False,
        nullable=False
    )

    comments = db.Column(
        db.Text,
        unique=False,
        nullable=True
    )

    replies = db.Column(
        db.Text,
        unique=False,
        nullable=True
    )

    parent_post = db.Column(
        db.String(12),
        unique=False,
        nullable=True
    )


class Image(db.Model):
    id = db.Column(
        db.String(12),
        primary_key=True,
        unique=True,
        nullable=False
    )

    author = db.Column(
        db.String(8),
        unique=False,
        nullable=False
    )

    parent_post = db.Column(
        db.String(12),
        unique=False,
        nullable=False
    )

    filename = db.Column(
        db.String(50),
        unique=False,
        nullable=False
    )

    sha256 = db.Column(
        db.String(44),
        unique=False,
        nullable=False
    )


class Comment(db.Model):
    id = db.Column(
        db.String(12),
        primary_key=True,
        unique=True,
        nullable=False
    )

    creation_time = db.Column(
        db.DateTime,
        unique=False,
        nullable=False
    )

    content = db.Column(
        db.Text,
        unique=False,
        nullable=False
    )

    parent_comment = db.Column(
        db.String(12),
        unique=False,
        nullable=True
    )

    parent_post = db.Column(
        db.String(12),
        unique=False,
        nullable=False
    )
