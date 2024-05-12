from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomAuthenticationForm, CustomerRegistrationForm, AddPlantForm, EditPlantForm, ReviewForm
from .models import *

# Create your views here.

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

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
    reviews = Review.objects.filter(plant=plant).all()
    total_review = 0
    if reviews:
        total = 0
        for review in reviews:
            total += review.rating
        total_review = total / len(reviews) * 1.0
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.plant = plant
            new_review.user = request.user
            new_review.date_posted = timezone.now()
            new_review.save()
            return redirect('details', plant_id=plant_id)

    context = {
        'plant': plant,
        'reviews': reviews,
        'form': form,
        'total_review': round(total_review, 1)
    }
    return render(request, 'details.html', context=context)


def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    plant.delete()
    return redirect('/plants')

def edit_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        form = EditPlantForm(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            if 'image' not in request.FILES:
                form.fields['image'].required = False
            form.save()
            return redirect('details', plant_id=plant_id)
        else:
            print(form.errors)
    else:
        form = EditPlantForm(instance=plant)

    return render(request, 'details.html', {'form': form})