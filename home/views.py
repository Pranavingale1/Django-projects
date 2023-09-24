from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    queryset = Recipe.objects.all()
    context = {'recipe':queryset}
    return render(request, 'home/index.html', context)

@login_required(login_url='/login/')
def add_recipe(request):
    if request.method == "POST":
        recipe_name = request.POST.get('recipe_name')
        recipe_description = request.POST.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')
        new = Recipe(recipe_name=recipe_name, recipe_description=recipe_description, recipe_image=recipe_image)
        new.save()
        messages.success(request, "New recipe added")
        return redirect('/')
    
    return render(request, 'home/add_recipe.html')

def delete_recipe(request, id):
    queryset = Recipe.objects.get(id = id)
    queryset.delete()
    return redirect('/')

def update_recipe(request, id):
    queryset = Recipe.objects.get(id = id)
    if request.method == "POST":
        recipe_name = request.POST.get('recipe_name')
        recipe_description = request.POST.get('recipe_description')
        recipe_image = request.FILES.get('recipe_image')

        queryset.recipe_name = recipe_name
        queryset.recipe_description = recipe_description

        if recipe_image:
            queryset.recipe_image = recipe_image

        queryset.save()
        
        return redirect('/')
    
    context = {'recipe':queryset}
    return render(request, 'home/update_recipe.html', context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.warning(request, 'Invalid username')
            return redirect('/login/')
        
        user = authenticate(username=username, password=password)

        if user is None:
            messages.warning(request, 'Password Invalid')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/')


    return render(request, 'home/login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

def Register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        
        if user.exists():
            messages.warning(request, 'Use different username')
            return redirect('/register/')
        
        user = User.objects.create(first_name=first_name, last_name=last_name, username=username)
        user.set_password(password)
        user.save()
        return render(request, 'home/login.html')
    return render(request, 'home/register.html')
    