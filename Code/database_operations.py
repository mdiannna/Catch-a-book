from app.models import User, Library, Book, BooksCarturesti



def addInitialLibraries():
	carturesti = Library(id=1, name='Carturesti')
	librarie_net = Library(id=2, name='Librarienet')
	db.session.add(carturesti)
	db.session.add(librarie_net)
	db.session.commit()

def moveBooksDataFromTables():
	carturesti_books = BooksCarturesti.query.all()
	for book in carturesti_books:
		new_book = Book(title=book.title, 
			author=book.author,
			isbn=book.isbn,
			link=book.link,
			editura=book.editura,
			price=book.price,
			library_id=1) 
		db.session.add(new_book)
		db.session.commit()
