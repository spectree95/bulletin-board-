from django import forms
from .models import Product,AttributeValue
from django.forms import inlineformset_factory


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "category", "subcategory"]
   
class AttributeValueForm(forms.ModelForm):
    class Meta:
        model = AttributeValue
        fields = ["value"]   
        
AttributeValueFormSet = inlineformset_factory(
    Product,
    AttributeValue,
    form=AttributeValueForm,
    extra=0)
