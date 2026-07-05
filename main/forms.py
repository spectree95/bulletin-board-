from django import forms
from .models import Product,AttributeValue
from django.forms import inlineformset_factory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "category", "subcategory", "description",'author']
        widgets = {
            
            "name" : forms.TextInput(attrs={
                "class": "input-field",
                "placeholder": "Дайте краткое описание товара",
                "style": "width: 700px; padding-left: 10px;border: 1.5px solid gray;border-radius: 3px;",
            }),
            "price" : forms.NumberInput(attrs={"placeholder" : "0.00"}),
            "description" : forms.Textarea(attrs={
                'placeholder' : "Напишите о деталях вашего продукта",
                "style" : "width: 700px;height: 150px; padding-left: 10px;border: 1.5px solid gray;border-radius: 3px;"
            })
        }
        
        
            
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get('subcategory')
        price = cleaned_data.get("price")
            
            
        if name and len(name) < 8:
            self.add_error("name", "Слишком короткое название.")
            
        if subcategory and subcategory and subcategory.category != category:
            self.add_error("subcategory","Подкатегория не принадлежит выбранной категории.")            
        
        if price is not None and price < 0:
            self.add_error("price", "Цена должна быть больше 0.")
            
        return cleaned_data    
        
        
   
class AttributeValueForm(forms.ModelForm):
    class Meta:
        model = AttributeValue
        fields = ["value"]   
        
AttributeValueFormSet = inlineformset_factory(
    Product,
    AttributeValue,
    form=AttributeValueForm,
    extra=0)
