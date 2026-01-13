from django.shortcuts import render, redirect, get_object_or_404
from .models import Property
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages

def about(request):
    return render(request, 'about.html')

def property_list(request):
    properties = Property.objects.all()

    location = request.GET.get('location')
    if location:
        properties = properties.filter(location__icontains=location)

    rooms = request.GET.get('rooms')
    if rooms:
        try:
            properties = properties.filter(rooms=int(rooms))
        except ValueError:
            pass

    price = request.GET.get('price')
    if price:
        try:
            properties = properties.filter(price__lte=int(price))
        except ValueError:
            pass

    return render(request, 'index.html', {'properties': properties})

def property_detail(request, id):
    property = get_object_or_404(Property, id=id)

    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                send_mail(
                    'Booking Confirmation',
                    f'Your booking for {property.title} is confirmed.',
                    'noreply@example.com',
                    [request.user.email],
                    fail_silently=True,
                )
                messages.success(request, 'Booking successful! Check your email.')
            except Exception as e:
                messages.success(request, 'Booking successful!')
            return redirect('/properties/')
        else:
            messages.error(request, 'Please login to book a property.')
            return redirect('/login/')

    return render(request, 'property_detail.html', {'property': property})

@login_required(login_url='/login/')
def add_property(request):
    if request.method == 'POST':
        try:
            Property.objects.create(
                owner=request.user,
                title=request.POST.get('title', ''),
                location=request.POST.get('location', ''),
                rooms=int(request.POST.get('rooms', 0)),
                price=int(request.POST.get('price', 0)),
                image=request.FILES.get('image')
            )
            messages.success(request, 'Property added successfully!')
            return redirect('/properties/')
        except Exception as e:
            messages.error(request, f'Error adding property: {str(e)}')
    return render(request, 'add_property.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match!')
            return redirect('/register/')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('/register/')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('/register/')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Registration successful! Please login.')
            return redirect('/login/')
        except Exception as e:
            messages.error(request, f'Error registering: {str(e)}')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('/properties/')
        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('/')

