from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.contrib.auth import login, logout

def getErrors(Forms):
    errors = []
    for form in Forms:
        for field, field_errors in form.errors.items():
            for error in field_errors:
                errors.append(f"{error}")
    return errors

# Create your views here.
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class Login(View):
    def get(self, request):
        form = AuthenticationForm()

        context = {
            'form' : form
        }

        return render(request, 'login.html', context)

    def post(self, request):
        form = AuthenticationForm(request=request, data=request.POST)


        if form.is_valid():
            user = form.get_user()

            login(request, user)
            return redirect('movies')
        
        context = {
            "form": form,
            "errors" : getErrors([form])
        }

        return render(request, 'login.html', context)
    
class Register(View):
    def get(self, request):
        form = CustomUserCreationForm()

        context = {
            'form' : form,
        }

        return render(request, 'register.html', context)
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            login(request, user)
            return redirect('/')
        
        context = {
            'form' : form,
            "errors" : getErrors([form])
        }

        return render(request, 'register.html', context)