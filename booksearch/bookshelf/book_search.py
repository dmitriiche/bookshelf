from django.db.models import Q
import requests

from .models import *


def init_search(string):
    search_in_public(string)


def search_in_db(search_string):
    authors = Author.objects.filter(Q(name__contains=search_string) |
                                    Q(second_name__contains=search_string) |
                                    Q(full_name__contains=search_string))

    books = Book.objects.get(Q(name__contains=search_string) |
                             Q(description__contains=search_string))

    if authors.count() <= 0 or books.count() <= 0:
        search_in_public(search_string)


def search_in_public(search_string):
    resp = requests.get(url="https://www.googleapis.com/books/v1/volumes", params={'q': search_string})

    resp.raise_for_status()

    data = resp.json()

    if 'totalItems' in data and data['totalItems']>0:
        parse_google_books_response(data)
    else:
        raise requests.exceptions.HTTPError


def parse_google_books_response(response_data):
    # get only 10 items from response
    items_count = response_data['totalItems'] if response_data['totalItems'] < 10 else 10
    items = response_data['items']
    books = [items[item] for item in range(0, items_count)]

    for book in books:
        # We get only first author from authors list
        try:
            author = Author.objects.get(full_name__contains=book['volumeInfo']['authors'][0])
        except Author.DoesNotExist:
            author = Author(full_name=book['volumeInfo']['authors'][0])
            author.save()

        Book(google_id=book['id'], name=book['volumeInfo']['title'],
             author=author, description=book['volumeInfo']['description'],
             image_url=book['volumeInfo']['imageLinks']['thumbnail']).save()



