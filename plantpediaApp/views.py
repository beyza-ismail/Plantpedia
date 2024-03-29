from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomAuthenticationForm, CustomerRegistrationForm, AddPlantForm
from .models import *

# Create your views here.

def index(request):
    return render(request, "index.html")


def all_plants(request):
    plants = Plant.objects.all()
    context = {"plants": plants}
    return render(request, "plants.html", context)

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')  # Redirect to the login page after successful registration
    else:
        form = CustomerRegistrationForm()
    return render(request, 'registration.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')

def add_plant(request):
    if request.method == 'POST':
        form = AddPlantForm(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save(commit=False)  # Create but don't save yet
            plant.user = request.user  # Set the user
            plant.save()  # Save the object with user assigned
            # Redirect to the book details page or any other appropriate URL
            return redirect('/plants')
    else:
        form = AddPlantForm()

    return render(request, 'add_plant.html', {'form': form})

def details(request, plant_id=None):
    plant = get_object_or_404(Plant, id=plant_id)

    context = {
        'plant': plant,
    }
    return render(request, 'details.html', context=context)