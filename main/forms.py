from django import forms
from .models import Product,AttributeValue
from django.forms import inlineformset_factory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "category", "subcategory"]
        
        def clean(self):
            cleaned_data = super().clean()
            name = cleaned_data.get("name")
            category = cleaned_data.get("category")
            subcategory = cleaned_data.get('subcategory')
            price = cleaned_data.get("price")
            
            
            if name and len(name) < 8:
                self.add_error("name", "Слишком короткое название.")
            
            if subcategory and subcategory and subcategory.category != category:
                raise forms.ValidationError("Подкатегория не принадлежит выбранной категории.")            
            
            if price and price < 0:
                self.add_error("Цена должна быть больше 0.")
            
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
