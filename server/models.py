from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, nullable=False)

    @validates("name")
    def validate_name(self, key, name):
        if not name or name.strip() == "":
            raise ValueError("Author must have a name")
        existing_author = Author.query.filter_by(name=name).first()
        if existing_author and existing_author != self:
            raise ValueError("Author name must be unique")
        return name

    @validates("phone_number")
    def validate_phone(self, key, phone):
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return phone


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, default="")
    category = db.Column(db.String, nullable=False)

    CLICKBAIT_WORDS = ["won't believe", "secret", "top", "guess"]

    @validates("title")
    def validate_title(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Post must have a title")
        # The title MUST contain at least one clickbait word
        lower_title = value.lower()
        if not any(word in lower_title for word in self.CLICKBAIT_WORDS):
            raise ValueError("Post title must be clickbait-y")
        return value

    @validates("content")
    def validate_content(self, key, value):
        if not value or len(value) < 250:
            raise ValueError("Content too short")
        return value

    @validates("summary")
    def validate_summary(self, key, value):
        if value and len(value) > 250:
            raise ValueError("Summary too long")
        return value

    @validates("category")
    def validate_category(self, key, value):
        if value not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Invalid category")
        return value
