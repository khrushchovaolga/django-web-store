from email.policy import default
from random import choices
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Cities, Order

class OrderCreateForm(forms.ModelForm):

    '''Для создания формы оформления заказа'''

    posts = (
        ('Nova Poshta', 'Нова пошта'),
        ('Ukrposhta' ,'Укрпошта'),
        ('Justin', 'Justin'),
        ('Meets' ,'Meets'),
    )

    first_name = forms.CharField(label=_("Customer name"), widget=forms.TextInput(attrs={'class':"input-field", 'placeholder':_("Customer name")}))
    last_name = forms.CharField(label=_('Surname'), widget=forms.TextInput(attrs={'class':"input-field", 'placeholder':_("Surname")}))
    number = forms.CharField(label=_('Number'), widget=forms.TextInput(attrs={'class':"input-field", 'placeholder':_("Number")}))
    email = forms.EmailField(label=_('Email'), widget=forms.EmailInput(attrs={'class':"input-field", 'placeholder':_("Email")}))
    #city = forms.ModelChoiceField(queryset=Cities.objects.all(), label=_('City'), widget=forms.Select(attrs={'class':"input-field", 'placeholder':_("City")}))
    #post = forms.MultipleChoiceField(choices=posts, label=_('Post'), widget=forms.Select(attrs={'class':"input-field", 'placeholder':_("Post")}))
    number_of_post = forms.CharField(label=_("Post number"), widget=forms.TextInput(attrs={'class':"input-field", 'placeholder':_("Post number")}))
    #call = forms.BooleanField(label=_("Don't call me"), widget=forms.CheckboxInput(attrs={'class':"input-field", 'placeholder':_("Don't call me")}))
    
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'number', 'email', 
        'city', 'post', 'number_of_post', 'call']