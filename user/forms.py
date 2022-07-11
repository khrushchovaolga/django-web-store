from dataclasses import fields
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class RegisterUserForm(UserCreationForm):

    '''Для создание формы регистрации пользователя'''

    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class':"input-field", 'placeholder':"Логін"}))
    email = forms.EmailField(label='Електронна пошта', widget=forms.EmailInput(attrs={'class':"input-field", 'placeholder':"Електронна пошта"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':"input-field", 'placeholder':"Пароль"}))
    password2 = forms.CharField(label='Підтвердження пароля', widget=forms.PasswordInput(attrs={'class':"input-field", 'placeholder':"Підтвердження пароля"}))


    class Meta: 
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class':"input-field", 'placeholder':"Логін"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':"input-field", 'placeholder':"Пароль"}))