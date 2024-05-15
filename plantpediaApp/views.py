from django.contrib.auth import logout, authenticate, login
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomAuthenticationForm, CustomerRegistrationForm, AddPlantForm, EditPlantForm, ReviewForm, \
    SearchForm
from .models import *

# Create your views here.

def index(request):
    plants = Plant.objects.annotate(avg_rating=Avg('review__rating'))
    plants = plants.order_by('-avg_rating')[:4]
    return render(request, "index.html", context={"plants": plants})

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def all_plants(request):
    # plants = Plant.objects.all()
    plants = Plant.objects.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating')
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


def search(request):
    query = request.GET.get('query', '')
    if query:
        plants = Plant.objects.filter(name__icontains=query)
        return render(request, 'results.html', {'plants': plants})
    else:
        return render(request, 'results.html', {'plants': []})


def faq(request):
    faq_items = [
        {
            'question': 'How do I create an account on Plantpedia?',
            'answer': 'To create an account on Plantpedia, click on the "Register" button located at the top right corner of the homepage. Fill out the required information, including your email address and a password, and follow the prompts to complete the registration process.'
        },
        {
            'question': 'How can I add a new plant to the Plantpedia database?',
            'answer': 'After logging in to your Plantpedia account, navigate to the "Add New Plant" section. Here, you can provide details about the plant, including its name, scientific name, description, care instructions, and upload a photo. Once you submit the information, the plant will be added to the Plantpedia database.'
        },
        {
            'question': 'Is it free to use Plantpedia?',
            'answer': 'Yes, Plantpedia is completely free to use for all users. There are no subscription fees or hidden charges associated with using the platform.'
        },
        {
            'question': 'How do I edit or delete a plant listing?',
            'answer': 'If you\'re the owner of the plant listing, you can edit or delete it by navigating to the plant\'s details page. From there, you\'ll find options to edit the plant details or delete the listing entirely.'
        },
        {
            'question': 'What should I do if I encounter an issue with the website?',
            'answer': 'If you encounter any issues while using the Plantpedia website, you can reach out to our customer support team for assistance. We strive to address any technical issues promptly to ensure a smooth user experience.'
        },
        {
            'question': 'How can I contact customer support?',
            'answer': 'You can contact our customer support team by emailing us at support@plantpedia.com or by filling out the contact form available on the website\'s "Contact" page.'
        },
        {
            'question': 'Can I sell plants on Plantpedia?',
            'answer': 'Plantpedia is primarily a platform for sharing information about plants and connecting plant enthusiasts. While you cannot directly sell plants on Plantpedia, you can use the platform to showcase plants you have available for sale and provide information about them.'
        },
        {
            'question': 'How do I leave a review for a plant?',
            'answer': 'To leave a review for a plant, navigate to the plant\'s details page and scroll down to the reviews section. Here, you can rate the plant and leave a comment based on your experience with it.'
        },
        {
            'question': 'Is my personal information secure on Plantpedia?',
            'answer': 'Yes, we take the security and privacy of our users\' personal information seriously. We employ robust security measures to protect user data and ensure that it is kept confidential.'
        },
        {
            'question': 'How do I reset my password if I forget it?',
            'answer': 'If you forget your password, you can reset it by clicking on the "Forgot Password" link on the login page. Follow the instructions provided, and a password reset link will be sent to your registered email address.'
        },
        {
            'question': 'Can I upload photos of my own plants to Plantpedia?',
            'answer': 'Yes, you can upload photos of your own plants to Plantpedia when adding new plant listings or leaving reviews. Simply follow the prompts to upload photos from your device.'
        },
        {
            'question': 'Are there any restrictions on the types of plants I can add to Plantpedia?',
            'answer': 'Plantpedia welcomes a wide variety of plant listings, including indoor plants, outdoor plants, flowers, trees, and more. However, we prohibit the listing of illegal or restricted plants that may pose environmental or legal risks.'
        },
        {
            'question': 'How often is the Plantpedia database updated?',
            'answer': 'The Plantpedia database is regularly updated with new plant listings and information. We strive to keep the database as current and comprehensive as possible to provide users with accurate and up-to-date plant information.'
        },
        {
            'question': 'Can I search for plants based on specific criteria, such as care level or sunlight requirements?',
            'answer': 'Yes, Plantpedia offers advanced search functionality that allows users to search for plants based on specific criteria such as care level, sunlight requirements, water needs, and more. Simply use the search filters provided to narrow down your search results.'
        },
        {
            'question': 'How do I navigate the Plantpedia website to find the information I need?',
            'answer': 'Plantpedia is designed to be user-friendly and intuitive, with easy navigation menus and search functionality. You can use the main navigation menu at the top of the page to explore different sections of the website, or use the search bar to find specific plants or topics of interest. Additionally, our FAQ section provides answers to common questions and can help guide you through the website.'
        }
    ]

    return render(request, "faq.html", {"faq_items": faq_items})
