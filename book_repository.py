from book import Book

class BookRepository:

    def __init__(self, connection):
        self._connection = connection

    def all(self):
        rows = self._connection.execute('SELECT * from books')
        books = []
        for row in rows:
            item = Book(row["id"], row["title"], row["author"], row["img_url"])
            books.append(item)
        return books

    def create(self, book):
        self._connection.execute(
            'INSERT INTO books (title, author, img_url) VALUES (%s, %s, %s)', [book.title, book.author, book.img_url])
        return None