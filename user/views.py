from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

from topikstore.utils import get_user_context

from .forms import *
from orders.models import *

'''def register(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('user:profile')
    else:
        form = UserCreationForm()

    context = get_user_context(
        form = form,
    )

    return render(request, 'registration/register.html', context)'''

class RegisterUser(CreateView):

    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('user:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_user_context(
            title = 'Реєстрація'
        ))
        return context

class LoginUser(LoginView):

    form_class = LoginUserForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('user:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_user_context(
            title = 'Авторизація'
        ))
        return context

def profile(request):
    context = get_user_context()
    return render(request, 'user/profile.html', context)

def order_history(request):

    orders = Order.objects.filter(user=request.user.id)
    print(request.user.id)
    context = get_user_context(
        orders = orders
    )
    return render(request, 'user/order_history.html', context)