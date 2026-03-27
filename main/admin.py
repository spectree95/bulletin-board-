from django.contrib import admin
from .models import Category,SubCategory,Liked, Product, Attribute,AttributeValue
# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(Product)
admin.site.register(Liked)
