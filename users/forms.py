from django import forms
from .models import User

from django.contrib.auth.forms import UserCreationForm


class CustomUserForm(UserCreationForm):
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))
        
    class Meta:
        model = User
        fields = ('username','last_name','first_name','email','phone_number','password1','password2')
        widgets = {
            'username' : forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
            'last_name' : forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email'
            }),
            'phone_number' :  forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефона'
            })
        }
        
        