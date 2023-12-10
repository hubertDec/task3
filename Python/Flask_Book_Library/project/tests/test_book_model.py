from unittest import TestCase
from project.books.models import Book
from parameterized import parameterized
from project import db, app

class TestBookModel(TestCase):

    def setUp (self):
       with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()


    @parameterized.expand([("1984", "George Orwell", 1948, "dystopia", "available"),
                           ("Książka", "Autor", 2023, "komedia", "unavailable"),
                           ("Practical Iot Hacking", "Chatzis Stais", 2021, "dramat", "stolen")])
    def test_correct_book_data(self, name: str, author: str, year_published: int, book_type: str, status: str):
        created_book = Book(name, author, year_published, book_type, status)
        with app.app_context():
            db.session.add(created_book)
            db.session.commit()


    @parameterized.expand([(1984, "George Orwell", 1948, "dystopia", "available"),
                           ("Książka", 123, 2023, "komedia", "unavailable"),
                           ("Practical Iot Hacking", "Chatzis Stais", "2021", "dramat", "stolen"),
                           ("Pentesting Basics", "Jan kowalski", 1800, 2010, "available"),
                           ("Dzieci z Bullerbyn", "Szwed szwedowski", 1337,"bajka", 9999)])
    def test_incorrect_book_data(self, name, author, year_published, book_type, status):
        created_book = Book(name, author, year_published, book_type, status)
        with app.app_context():
            db.session.add(created_book)
            self.assertRaises(Exception, db.session.commit())

    
    @parameterized.expand([("1"*1000000, "George Orwell", 1948, "dystopia", "available"),
                           ("Książka", "1"*1000000, 2023, "komedia", "unavailable"),
                           ("Practical Iot Hacking", "Chatzis Stais", 2021000000000000000000000, "dramat", "stolen"),
                           ("Pentesting Basics", "Jan kowalski", 1800, "1"*1000000, "available"),
                           ("Dzieci z Bullerbyn", "Szwed szwedowski", 1337,"bajka",  "1"*1000000)])
    def test_extreme_book_data(self, name, author, year_published, book_type, status):
        created_book = Book(name, author, year_published, book_type, status)
        with app.app_context():
            db.session.add(created_book)
            self.assertRaises(Exception, db.session.commit())
    

    @parameterized.expand([("1984 union select 1 -- -", "George Orwell", 1948, "dystopia", "available"),
                           ("Książka", "Autor union select 1 -- -", 2023, "komedia", "unavailable"),
                           ("Practical Iot Hacking", "Chatzis Stais", "2021 union select 1 -- -", "dramat", "stolen"),
                           ("Pentesting Basics", "Jan kowalski", 1800, "gatunek union select 1 -- -", "available"),
                           ("Dzieci z Bullerbyn", "Szwed szwedowski", 1337,"bajka", "unavailable union select 1 -- -")])
    def test_sql_injection(self, name, author, year_published, book_type, status):
        created_book = Book(name, author, year_published, book_type, status)
        with app.app_context():
            db.session.add(created_book)
            self.assertRaises(Exception, db.session.commit())
        

    @parameterized.expand([("<script>alert(1)</script>", "George Orwell", 1948, "dystopia", "available"),
                           ("Książka", "<script>alert(1)</script>", 2023, "komedia", "unavailable"),
                           ("Practical Iot Hacking", "Chatzis Stais", "<script>alert(1)</script>", "dramat", "stolen"),
                           ("Pentesting Basics", "Jan kowalski", 1800, "<script>alert(1)</script>", "available"),
                           ("Dzieci z Bullerbyn", "Szwed szwedowski", 1337,"bajka", "<script>alert(1)</script>")])
    def test_xss(self, name, author, year_published, book_type, status):
        created_book = Book(name, author, year_published, book_type, status)
        with app.app_context():
            db.session.add(created_book)
            self.assertRaises(Exception, db.session.commit())