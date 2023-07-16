from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
    return JsonResponse({'Hello': "This is a little Lemon."})