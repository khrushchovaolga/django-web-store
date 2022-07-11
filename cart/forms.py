from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        coerce=int, 
        choices=PRODUCT_QUANTITY_CHOICES,
    )
    #volume = forms.CharField(IsAvailableVolumeProduct.objects.all())
    update = forms.BooleanField(
        required=False, 
        initial=False,
        widget=forms.HiddenInput
    )