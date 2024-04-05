from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

# Define the path to your SQLite database file
DATABASE = 'db/books.db'

# API to get all authors
@app.route('/api/authors', methods=['GET'])
def get_all_authors():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Authors")
        authors = cursor.fetchall()
        conn.close()
        return jsonify(authors)
    except Exception as e:
        return jsonify({'error': str(e)})

# API to get all reviews
@app.route('/api/reviews', methods=['GET'])
def get_all_reviews():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Reviews")
        reviews = cursor.fetchall()
        conn.close()
        return jsonify(reviews)
    except Exception as e:
        return jsonify({'error': str(e)})

# API to add a book to the database
@app.route('/api/add_book', methods=['POST'])
def add_book():
    # Connect to your SQLite database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    data = request.json
    title = data['title']
    publication_year = data['year']
    authors = data['authors']  # This comes as a list of author names

    # Insert the new book
    cursor.execute("INSERT INTO Books (title, publication_year) VALUES (?, ?)", (title, publication_year))
    book_id = cursor.lastrowid  # Get the id of the last inserted book

    for author_name in authors:
        # Check if the author exists
        cursor.execute("SELECT author_id FROM Authors WHERE name = ?", (author_name,))
        author = cursor.fetchone()

        if author is None:
            # If the author doesn't exist, insert the new author
            cursor.execute("INSERT INTO Authors (name) VALUES (?)", (author_name,))
            author_id = cursor.lastrowid
        else:
            # If the author exists, use the existing author's id
            author_id = author[0]

        # Insert into book_author table
        cursor.execute("INSERT INTO book_author (book_id, author_id) VALUES (?, ?)", (book_id, author_id))

    # Commit the changes to the database
    conn.commit()
    conn.close()

    return jsonify({'status': 'Book and Authors added successfully'})

@app.route('/api/search_books', methods=['GET'])
def search_books_by_year():
    year = request.args.get('year')
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Use a JOIN to fetch books along with their authors
        cursor.execute("""
            SELECT b.title, b.publication_year, GROUP_CONCAT(a.name, ', ') AS authors
            FROM Books b
            LEFT JOIN book_author ba ON b.book_id = ba.book_id
            LEFT JOIN Authors a ON ba.author_id = a.author_id
            WHERE b.publication_year = ?
            GROUP BY b.title, b.publication_year
        """, (year,))
        
        books = cursor.fetchall()

        # Convert the result into a list of dictionaries
        books_list = [{'title': book[0], 'publication_year': book[1], 'authors': book[2] or 'No Authors Listed'} for book in books]

        conn.close()

        if books_list:
            return jsonify({'books': books_list})
        else:
            return jsonify({'message': 'No books found for the specified year.'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500




# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# API to fetch all books with authors
@app.route('/api/books', methods=['GET'])
def get_all_books_with_authors():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.book_id, b.title, b.publication_year, GROUP_CONCAT(a.name, ', ') as authors
            FROM Books b
            LEFT JOIN book_author ba ON b.book_id = ba.book_id
            LEFT JOIN Authors a ON ba.author_id = a.author_id
            GROUP BY b.book_id
        """)
        books = cursor.fetchall()
        book_list = [{'book_id': book[0], 'title': book[1], 'publication_year': book[2], 'authors': book[3]} for book in books]
        conn.close()
        return jsonify({'books': book_list})
    except Exception as e:
        return jsonify({'error': str(e)})
