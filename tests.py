# test_books_collector.py
import pytest
from main import BooksCollector

@pytest.fixture
def bc():
    return BooksCollector()

@pytest.mark.parametrize("name,should_add", [
    ("Книга ровно 40 символов " + "x"*(40-22), True),
    ("Ок", True),
    ("", False),
    ("x"*41, False),
])
def test_add_new_book_length_rules(bc, name, should_add):
    bc.add_new_book(name)
    assert (name in bc.get_books_genre()) is should_add

def test_add_new_book_no_duplicates(bc):
    bc.add_new_book("Дюна")
    bc.add_new_book("Дюна")
    assert list(bc.get_books_genre().keys()).count("Дюна") == 1

def test_set_book_genre_success(bc):
    bc.add_new_book("Дюна")
    bc.set_book_genre("Дюна", "Фантастика")
    assert bc.get_book_genre("Дюна") == "Фантастика"

def test_set_book_genre_ignored_if_invalid_genre(bc):
    bc.add_new_book("Дюна")
    bc.set_book_genre("Дюна", "Несуществующий жанр")
    assert bc.get_book_genre("Дюна") == ""  # жанр не меняется

def test_set_book_genre_ignored_if_no_book(bc):
    bc.set_book_genre("Нет такой книги", "Фантастика")
    assert bc.get_book_genre("Нет такой книги") is None

def test_get_books_with_specific_genre_returns_only_that_genre(bc):
    bc.add_new_book("Дюна"); bc.set_book_genre("Дюна", "Фантастика")
    bc.add_new_book("Ит"); bc.set_book_genre("Ит", "Ужасы")
    assert bc.get_books_with_specific_genre("Фантастика") == ["Дюна"]

def test_get_books_with_specific_genre_empty_if_none(bc):
    bc.add_new_book("Дюна"); bc.set_book_genre("Дюна", "Фантастика")
    assert bc.get_books_with_specific_genre("Комедии") == []

def test_get_books_genre_returns_dict(bc):
    bc.add_new_book("Дюна"); bc.set_book_genre("Дюна", "Фантастика")
    bc.add_new_book("Маска"); bc.set_book_genre("Маска", "Комедии")
    assert bc.get_books_genre() == {"Дюна": "Фантастика", "Маска": "Комедии"}

def test_get_books_for_children_excludes_age_restricted(bc):
    bc.add_new_book("Ит"); bc.set_book_genre("Ит", "Ужасы")
    bc.add_new_book("Шерлок"); bc.set_book_genre("Шерлок", "Детективы")
    bc.add_new_book("Коко"); bc.set_book_genre("Коко", "Мультфильмы")
    result = bc.get_books_for_children()
    assert "Коко" in result and "Ит" not in result and "Шерлок" not in result

def test_add_book_in_favorites_only_existing(bc):
    bc.add_new_book("Дюна")
    bc.add_book_in_favorites("Дюна")
    bc.add_book_in_favorites("Неизвестная")  # игнор
    assert bc.get_list_of_favorites_books() == ["Дюна"]

def test_add_book_in_favorites_no_duplicates(bc):
    bc.add_new_book("Дюна")
    bc.add_book_in_favorites("Дюна")
    bc.add_book_in_favorites("Дюна")
    assert bc.get_list_of_favorites_books().count("Дюна") == 1

def test_delete_book_from_favorites(bc):
    bc.add_new_book("Дюна")
    bc.add_book_in_favorites("Дюна")
    bc.delete_book_from_favorites("Дюна")
    assert bc.get_list_of_favorites_books() == []
