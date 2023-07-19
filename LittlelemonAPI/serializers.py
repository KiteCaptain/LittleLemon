from rest_framework import serializers
from LittlelemonAPI.models import MenuItem, Category
# Category
from decimal import Decimal 

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