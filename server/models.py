from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.Integer)

    posts = db.relationship('Post', backref='author')

    @validates('name')
    def validate_name(self, key, name):
        author_names = db.session.query(Author.name).all()
        if not name:
            raise ValueError('Please provide a name')
        elif name in author_names:
            raise ValueError('Please provide a unique name')
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):        
        if len(phone_number) != 10:
            raise ValueError('Please provide 10 digit phone number')
        return phone_number

    def __repr__(self):
        return f'<Author {self.name}/>'


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    summary = db.Column(db.String)
    category = db.Column(db.String)

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    @validates('title')
    def validate_title(self, key, title):
        bait_list = ["Won't Believe", "Secrets", "Top [numbers]", "Guess"]
        if not title:
            raise ValueError('Please provide a title')
        elif title not in bait_list:
        # elif not any(bait in title for bait in bait_list):
        # ^this is Generator Expression which is more memory efficient!!!!!
            raise ValueError('Please provide a clickbait-y title')
        return title
    
    @validates('content')
    def validate_content(self, key, content):        
        if len(content) <= 250:
            raise ValueError('Content too short. Needs more than 250 chars')
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):        
        if len(summary) > 250:
            raise ValueError('Summary too long. Must be less than 250 chars')
        return summary

    @validates('category')
    def validate_category(self, key, category):        
        if category != 'Fiction' or category != 'Non_Fiction': 
            raise ValueError('Incorrect category')
        return category

    def __repr__(self):
        return f'<Post {self.title}/>'