from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'number', 'email', 
        'city', 'post', 'number_of_post']
        
        