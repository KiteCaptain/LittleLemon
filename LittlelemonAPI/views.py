from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from .models import MenuItem , Category
from .serializers import MenuItemSerializer, CategorySerializer
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated 
from rest_framework.decorators import permission_classes 
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
from .throttles import TenCallsPerMinute
from rest_framework.permissions import IsAdminUser 
from django.contrib.auth.models import User, Group

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
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering =request.query_params.get('ordering')
        perpage =request.query_params.get('perpage', default=2)
        page =request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price) # __lte means less than or equal to
        if search:
            items = items.filter(title__icontains=search) 
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields) 
        paginator = Paginator(items,per_page=perpage)
        try:
            items = paginator.page(number=page) 
        except EmptyPage:
            items = []
            
        serialized_item = MenuItemSerializer(items, many=True)
        return (Response(serialized_item.data))
    
    elif request.method == 'POST':
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

## User Roles
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "Some secret message"})
    
@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message": "Some secret message, ONLY FOR THE MANAGER!"})
    else:
        return Response({"message": "You are not authorized"})
    


# Adding users to a group
@api_view()
@permission_classes([IsAdminUser])
def managers(request):   
    username = request.data['username']
    if username: 
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        if request.method == 'POST':
            managers.user_set.add(user)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response({"message": "OKAY"})
    return Response({"message": "ERROR"}, status.HTTP_400_BAD_REQUEST)
            
    
    
# Throttling 
@api_view()
@throttle_classes([UserRateThrottle])
def throttle_check(request):
    return Response({"message": "successful"})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({"message": "Authenticated throttle limit unreached successful"})


# {
# 	"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5MDE5NDA2MSwiaWF0IjoxNjkwMTA3NjYxLCJqdGkiOiIxMzY0Njc0NDJhZWM0MDA2ODI5ZGUyZDhjNjdkMjlhZCIsInVzZXJfaWQiOjJ9.vyp-SUZmsbek1SReR1LnuerAoKjxNg9sacRpuIriJoI",
# 	"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkwMTA3OTYxLCJpYXQiOjE2OTAxMDc2NjEsImp0aSI6ImNmNzY3ZTgzNWEyYjRjMDdiM2ViYjk2NWZhZjRhZmRmIiwidXNlcl9pZCI6Mn0.lFBtM_aRcE3_RhqBxKRWQQbsOSaVwU_M6mREhp7r_NY"
# }