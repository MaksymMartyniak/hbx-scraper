from rest_framework import serializers
from .models import Clothing, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['title', 'gender', 'url', "code"]


class ClothingSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Clothing
        fields = ["sku", "title", "brand", "price", "category", "url", "img"]
