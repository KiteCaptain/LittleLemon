from rest_framework import serializers
from LittlelemonAPI.models import MenuItem, Category
from decimal import Decimal 
import bleach



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = ['id', 'slug', 'title']

# class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # category = CategorySerializer()
    # category = serializers.HyperlinkedRelatedField(
    #     querysery = Category.objects.all(),
    #     view_name = 'category-detail'
    # )
    
    ## DATA VALIDATION 
    # Using the validate method to validate multiple fields at once
    # def validate(self, attrs):
    #     if(attrs['price']<2):
    #         raise serializers.ValidationError('Price should not be less than 2.0')
    #     if(attrs['inventory']<0):
    #         raise serializers.ValidationError('Stock cannot be negative')
    #     return super().validate(attrs)
    
    # Using validate field method()
    def validate_title(self, value):
        return bleach.clean(value)
    def validate_price(self, value):
        if (value < 2):
            raise serializers.ValidationError('Price should not be less than 2.0')
    def validate_stock(self, value):
        if (value < 0):
            raise serializers.ValidationError('Stock cannot be negative')
        
    class Meta:
        model = MenuItem 
        fields = [
            'id',
            'title',
            'price',
            'stock',
            'price_after_tax',
            'category',
        ]
        # depth =1
        
    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)
    dci = {
        "title": "beef steak",
        "price": "2.50",
        "stock": 100,
    }