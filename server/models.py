from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author name cannot be empty")
        
        # Check for existing author with same name
        existing_author = db.session.query(Author).filter(Author.name == name).first()
        if existing_author:
            raise ValueError("Author name must be unique")
        
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number:
            # Remove any non-digit characters
            digits_only = re.sub(r'\D', '', phone_number)
            if len(digits_only) != 10:
                raise ValueError("Phone number must be exactly 10 digits")
            return digits_only
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    VALID_CATEGORIES = ['Fiction', 'Non-Fiction']
    CLICKBAIT_PHRASES = ['Won\'t Believe', 'Secret', 'Top', 'Guess']

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post title cannot be empty")
        
        if not any(phrase.lower() in title.lower() for phrase in self.CLICKBAIT_PHRASES):
            raise ValueError("Title must contain one of the following phrases: " + 
                           ", ".join(self.CLICKBAIT_PHRASES))
        return title

    @validates('content')
    def validate_content(self, key, content):
        if content and len(content) < 250:
            raise ValueError("Content must be at least 250 characters long")
        return content

    @validates('category')
    def validate_category(self, key, category):
        if category not in self.VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(self.VALID_CATEGORIES)}")
        return category

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Summary cannot exceed 250 characters")
        return summary

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'