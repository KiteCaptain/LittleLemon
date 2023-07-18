from django.shortcuts import render
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.decorators import api_view
from rest_framework.views import APIView 
from django.http import JsonResponse
from .models import Book
import random

# My Views
def index(request):
    return JsonResponse({'Hello': "This is for the booklist API."})

@api_view(['GET','POST'])
def books(request):
    if request.method == 'POST':
        return Response('list of books(POST)', status=status.HTTP_200_OK)
    return Response('list of books(GET)', status=status.HTTP_200_OK)

class BookList(APIView):
    def get(self, request):
        return Response({"msg": "List of books(GET)"}, status=status.HTTP_200_OK)    
    def post(self, request):
        return Response({"msg": "Updated booklist(POST)"}, status=status.HTTP_200_OK)


@csrf_exempt
def book_list(request):
    books = Book.objects.all()
    if books:
        book_list = [model_to_dict(book) for book in books]
        return JsonResponse(book_list, safe=False)
    else:
        return JsonResponse({'Hello': "Books List not found"})
    
@csrf_exempt
def book_details(request, id):
    ran_id = random.randint(1,5)
    try:
        book = Book.objects.get(pk=ran_id)
    except Exception as e:
        return JsonResponse({"error": "THE REQUEST BOOK DOES NOT EXIST, 404 BABY :("})
        
    if book:
        return JsonResponse(model_to_dict(book), safe=False)