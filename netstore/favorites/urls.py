from django.urls import path
from .views import *

app_name = 'favorites'

urlpatterns = [
    path('', favorites_detail, name = 'favorites_detail'),
    path('add/<int:product_pk>', favorites_add, name = 'favorites_add'),
    path('remove/<int:product_pk>', favorites_remove, name = 'favorites_remove'),
]