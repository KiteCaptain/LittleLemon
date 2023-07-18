from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name="index"),
    # path('books/', views.books),
    path('books/', views.BookList.as_view()),
    path('api/books/', views.book_list, name="book-list"),
    path('api/books/<str:id>/', views.book_details, name="book-details"),
]
