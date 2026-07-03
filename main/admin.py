from django.contrib import admin
from .models import Category,SubCategory,Liked, Product, Attribute,AttributeValue,ProductImage
# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(Liked)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug' : ('name', 'id')}