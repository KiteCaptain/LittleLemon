from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MenuItem , Category
from .serializers import MenuItemSerializer, CategorySerializer

# # Class based views
# class MenuItemsView(generics.ListCreateAPIView):
#     # queryset = MenuItem.objects.select_related('category').all() 
#     queryset = MenuItem.objects.select_related().all() 
#     serializer_class = MenuItemSerializer 
    
# class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer


    
# Function based views
@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all() 
        serialized_item = MenuItemSerializer(items, many=True)
        return (Response(serialized_item.data))
    if request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        # serialized_item.validated_data
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)
        

@api_view()
def single_item(request, id):
    items = get_object_or_404(MenuItem,pk=id)
    serialized_item = MenuItemSerializer(items)
    return (Response(serialized_item.data))

@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk) 
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)
    
    