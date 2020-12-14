from django.http import HttpResponse
from django.shortcuts import render
from .book_search import init_search

# Create your views here.

def search(request):
    if request.method == 'GET' and 'q' in request.GET:
        search_string = request.GET.get('q')
    print(search_string)
    if search_string:
        init_search(search_string)

    return HttpResponse("You're looking at question .")
