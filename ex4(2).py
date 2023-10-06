import sqlite3


conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# 创建表格
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        BookID INTEGER PRIMARY KEY,
        Title TEXT,
        Author TEXT,
        ISBN TEXT,
        Status TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID INTEGER PRIMARY KEY,
        Name TEXT,
        Email TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reservations (
        ReservationID INTEGER PRIMARY KEY,
        BookID INTEGER,
        UserID INTEGER,
        ReservationDate TEXT,
        FOREIGN KEY (BookID) REFERENCES Books (BookID),
        FOREIGN KEY (UserID) REFERENCES Users (UserID)
    )
''')


def add_book(title, author, isbn, status):
    cursor.execute('''
        INSERT INTO Books (Title, Author, ISBN, Status)
        VALUES (?, ?, ?, ?)
    ''', (title, author, isbn, status))
    conn.commit()


def find_book_details(book_id):
    cursor.execute('''
        SELECT Books.*, Users.Name, Reservations.ReservationDate
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
        WHERE Books.BookID = ?
    ''', (book_id,))
    result = cursor.fetchone()
    if result:
        print("BookID:", result[0])
        print("Title:", result[1])
        print("Author:", result[2])
        print("ISBN:", result[3])
        print("Status:", result[4])
        print("Reserved by:", result[6] if result[6] else "Not reserved")
        print("Reservation Date:", result[7] if result[7] else "Not reserved")
    else:
        print("Book not found")

def find_reservation_status(criteria):
    if criteria.startswith('LB'):
       
        cursor.execute('''
            SELECT Books.*, Users.Name, Reservations.ReservationDate
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Books.BookID = ?
        ''', (int(criteria[2:]),))
    elif criteria.startswith('LU'):
       
        cursor.execute('''
            SELECT Books.*, Users.Name, Reservations.ReservationDate
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Users.UserID = ?
        ''', (int(criteria[2:]),))
    elif criteria.startswith('LR'):
        
        cursor.execute('''
            SELECT Books.*, Users.Name, Reservations.ReservationDate
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Reservations.ReservationID = ?
        ''', (int(criteria[2:]),))
    else:
       
        cursor.execute('''
            SELECT Books.*, Users.Name, Reservations.ReservationDate
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Books.Title = ?
        ''', (criteria,))
    
    result = cursor.fetchone()
    if result:
        print("BookID:", result[0])
        print("Title:", result[1])
        print("Author:", result[2])
        print("ISBN:", result[3])
        print("Status:", result[4])
        print("Reserved by:", result[6] if result[6] else "Not reserved")
        print("Reservation Date:", result[7] if result[7] else "Not reserved")
    else:
        print("Book not found")


def find_all_books():
    cursor.execute('''
        SELECT Books.*, Users.Name, Reservations.ReservationDate
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
    ''')
    results = cursor.fetchall()
    if results:
        for result in results:
            print("BookID:", result[0])
            print("Title:", result[1])
            print("Author:", result[2])
            print("ISBN:", result[3])
            print("Status:", result[4])
            print("Reserved by:", result[6] if result[6] else "Not reserved")
            print("Reservation Date:", result[7] if result[7] else "Not reserved")
            print("--------------")
    else:
        print("No books found")


def update_book_details(book_id, new_status):
    cursor.execute('''
        UPDATE Books
        SET Status = ?
        WHERE BookID = ?
    ''', (new_status, book_id))
    cursor.execute('''
        UPDATE Reservations
        SET ReservationDate = NULL
        WHERE BookID = ?
    ''', (book_id,))
    conn.commit()


def delete_book(book_id):
    cursor.execute('''
        DELETE FROM Books
        WHERE BookID = ?
    ''', (book_id,))
    cursor.execute('''
        DELETE FROM Reservations
        WHERE BookID = ?
    ''', (book_id,))
    conn.commit()


while True:
    print("1. Add a new book")
    print("2. Find a book's detail based on BookID")
    print("3. Find a book's reservation status")
    print("4. Find all books in the database")
    print("5. Modify/update book details")
    print("6. Delete a book")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        title = input("Enter the title: ")
        author = input("Enter the author: ")
        isbn = input("Enter the ISBN: ")
        status = input("Enter the status: ")
        add_book(title, author, isbn, status)
    elif choice == '2':
        book_id = int(input("Enter the BookID: "))
        find_book_details(book_id)
    elif choice == '3':
        criteria = input("Enter BookID, Title, UserID, or ReservationID: ")
        find_reservation_status(criteria)
    elif choice == '4':
        find_all_books()
    elif choice == '5':
        book_id = int(input("Enter the BookID: "))
        new_status = input("Enter the new status: ")
        update_book_details(book_id, new_status)
    elif choice == '6':
        book_id = int(input("Enter the BookID: "))
        delete_book(book_id)
    elif choice == '7':
        break