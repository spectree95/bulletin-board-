from django.contrib import admin
from .models import Category,SubCategory,Liked, Product, Attribute,AttributeValue,ProductImage,AttributeValue
# Register your models here.


admin.site.register(AttributeValue)
admin.site.register(Liked)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug' : ('name',)}
    
    
    
class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1
    fields = ("name", )  # какие поля показывать в таблице

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "subcategory_count")
    inlines = [SubCategoryInline]

    def subcategory_count(self, obj):
        return obj.subcategory_set.count()
    subcategory_count.short_description = "Кол-во подкатегорий"
    
    
class AttributeInline(admin.TabularInline):
    model = Attribute
    extra = 1
    fields = ("name", "attr_type")

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "attribute_count")
    list_filter = ("category",)
    inlines = [AttributeInline]

    def attribute_count(self, obj):
        return obj.attributes.count()
    attribute_count.short_description = "Атрибутов"    
    
    