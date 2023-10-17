from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref='books')

class AuthorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        include_fk = True

class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        include_fk = True

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route('/authors', methods=['POST'])
def add_author():
    name = request.json['name']
    new_author = Author(name=name)
    db.session.add(new_author)
    db.session.commit()
    return author_schema.jsonify(new_author)

@app.route('/authors', methods=['GET'])
def get_authors():
    authors = Author.query.all()
    return authors_schema.jsonify(authors)

@app.route('/books', methods=['POST'])
def add_book():
    title = request.json['title']
    author_id = request.json['author_id']
    new_book = Book(title=title, author_id=author_id)
    db.session.add(new_book)
    db.session.commit()
    return book_schema.jsonify(new_book)

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return books_schema.jsonify(books)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0')
