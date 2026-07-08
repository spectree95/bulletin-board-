from django.db import models
from bulletin_board import settings
import os
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

def get_slug_to_upload__path(instance,filename):
    if instance:
        return os.path.join('products', instance.product.slug, filename)
    
    

class Category(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name



class SubCategory(models.Model):
    name = models.CharField(max_length=50, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    img = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'



class Attribute(models.Model):
    name = models.CharField(max_length=50)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="attributes")
    
    ATTRIBUTE_TYPES = [
        ("text", "Текст"),
        ("number", "Число"),
    ]
    attr_type = models.CharField(max_length=10, choices=ATTRIBUTE_TYPES, default="text")

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE, related_name="products")
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=20,decimal_places=2,blank=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            self.slug = f"{slugify(self.name)}-{self.pk}"
            super().save(update_fields=['slug'])    
    
    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(
        upload_to=get_slug_to_upload__path,
        validators=[FileExtensionValidator(
            allowed_extensions=["png", 'jpeg', 'jpg', 'svg', 'raw', 'webp', 'tiff']
        )]
    )
    
    
    
class AttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)
    
    
    def clean(self):
        cleaned_data = super().clean()
        
        if self.attribute.attr_type == "number":
            try:
                if float(self.value) <= 0:
                    raise ValidationError({
                        "value": f"Значение атрибута {self.attribute.name} должно быть больше 0."
                    })
            except (TypeError, ValueError):
                raise ValidationError({
                    "value": f"Значение атрибута {self.attribute.name} должно быть числом."
                })
        return cleaned_data
        
    class Meta:
        unique_together = ('product','attribute')
    



class Liked(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.username}, {self.product}"    