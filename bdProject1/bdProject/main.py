import pymysql
import pymysql.cursors
from config import host, user, password, db_name

try:
    connection = pymysql.connect(
        host=host,
        port=33060,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Successfully connected...")
except Exception as ex:
    print("Connection refused...")
    print(ex)

try:
    with connection.cursor() as cursor:
        # Ввод данных для таблицы book
        title = input("Enter book title: ")
        author = input("Enter author's name: ")
        year = input("Enter year of publication (YYYY-MM-DD): ")
        status = input("Enter book status (available/unavailable): ")
        
        insert_book_query = "INSERT INTO library_management_system.book (title, author, year, status) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_book_query, (title, author, year, status))
        book_id = cursor.lastrowid  # Получаем ID только что вставленной книги

        # Ввод данных для таблицы genre
        genre_name = input("Enter genre name: ")
        select_genre_query = "SELECT id FROM library_management_system.genre WHERE name = %s"
        cursor.execute(select_genre_query, (genre_name,))
        result = cursor.fetchone()
        if result:
            genre_id = result['id']
        else:
            insert_genre_query = "INSERT INTO library_management_system.genre (name) VALUES (%s)"
            cursor.execute(insert_genre_query, (genre_name,))
            genre_id = cursor.lastrowid  # Получаем ID только что вставленного жанра

        # Ввод данных для таблицы book_genre
        insert_book_genre_query = "INSERT INTO library_management_system.book_genre (book_id, genre_id) VALUES (%s, %s)"
        cursor.execute(insert_book_genre_query, (book_id, genre_id))

        connection.commit()
        print("Data inserted successfully")

        # Выбор всех данных из таблицы book
        select_book_query = "SELECT * FROM library_management_system.book"
        cursor.execute(select_book_query)
        result = cursor.fetchall()
        for row in result:
            print(row)

except Exception as ex:
    print("Failed to insert data into database")
    print(ex)
finally:
    connection.close()