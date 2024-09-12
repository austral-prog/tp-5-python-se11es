from typing import Optional
from src.Book import Book
from src.User import User
from datetime import datetime

class Library:
    def __init__(self):
        self.__books = []
        self.__users = []
        self.__checked_out_books = []
        self.__checked_in_books = []

    def get_books(self) -> List[Book]:
        return self.__books

    def get_users(self) -> List[User]:
        return self.__users

    def get_checked_out_books(self) -> List[List[Optional[str]]]:
        return self.__checked_out_books

    def get_checked_in_books(self) -> List[List[Optional[str]]]:
        return self.__checked_in_books

    def add_book(self, isbn: str, title: str, author: str) -> None:
        if any(book.get_isbn() == isbn for book in self.__books):
            print(f"Book with ISBN {isbn} already exists.")
            return
        new_book = Book(isbn, title, author)
        self.__books.append(new_book)
        print(f"Book '{title}' added successfully.")

    def list_all_books(self) -> None:
        for book in self.__books:
            print(book)

    def check_out_book(self, isbn: str, dni: int, due_date: str) -> None:
        book = next((b for b in self.__books if b.get_isbn() == isbn), None)
        if book is None:
            print(f"Unable to find the data for the values: ISBN {isbn} and DNI: {dni}")
            return

        user = next((u for u in self.__users if u.get_dni() == dni), None)
        if user is None:
            print(f"Unable to find the data for the values: ISBN {isbn} and DNI: {dni}")
            return

        if not book.is_available():
            print(f"Book {isbn} is not available")
            return

        if any(co[0] == isbn for co in self.__checked_out_books):
            print(f"Book {isbn} is already checked out")
            return

        self.__checked_out_books.append([isbn, dni, due_date])
        book.set_available(False)
        user.increment_checkouts()
        print(f"User {dni} checked out book {isbn}")

    def check_in_book(self, isbn: str, dni: int, returned_date: str) -> None:
        book = next((b for b in self.__books if b.get_isbn() == isbn), None)
        if book is None:
            print(f"Book {isbn} is not available")
            return

        checked_out = next((co for co in self.__checked_out_books if co[0] == isbn and co[1] == dni), None)
        if checked_out is None:
            print(f"Book {isbn} is not available")
            return

        self.__checked_in_books.append([isbn, dni, returned_date])
        self.__checked_out_books.remove(checked_out)
        book.set_available(True)
        user = next((u for u in self.__users if u.get_dni() == dni), None)
        if user:
            user.increment_checkins()
        print(f"Book {isbn} checked in successfully")

    def add_user(self, dni: int, name: str) -> None:
        if any(u.get_dni() == dni for u in self.__users):
            print(f"User with DNI {dni} already exists.")
            return
        new_user = User(dni, name)
        self.__users.append(new_user)
        print(f"User '{name}' added successfully.")
