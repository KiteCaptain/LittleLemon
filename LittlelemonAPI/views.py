from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import generics 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MenuItem  
from .serializers import MenuItemSerializer 

# Class based views
class MenuItemsView(generics.ListCreateAPIView):
    # queryset = MenuItem.objects.select_related('category').all() 
    queryset = MenuItem.objects.select_related().all() 
    serializer_class = MenuItemSerializer 
    
class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all() 
    serializer_class = MenuItemSerializer

# # Function based views
# @api_view()
# def menu_items(request):
#     items = MenuItem.objects.select_related('category').all() 
#     serialized_item = MenuItemSerializer(items, many=True)
#     return (Response(serialized_item.data))

# @api_view()
# def single_item(request, id):
#     items = get_object_or_404(MenuItem,pk=id)
#     serialized_item = MenuItemSerializer(items)
#     return (Response(serialized_item.data))