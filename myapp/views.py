from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import json

from .models import Property, UserProfile, BookingRequest, PropertyImage
from .forms import (
    UserRegistrationForm, UserProfileForm, HomeOwnerRegistrationForm, 
    HomeOwnerProfileForm, PropertyForm, PropertyImageForm, BookingRequestForm, 
    BookingResponseForm, PasswordResetForm
)


def about(request):
    return render(request, 'about.html')


def property_list(request):
    """Display list of all properties with search filters"""
    properties = Property.objects.all()
    
    # Search filters
    city = request.GET.get('city')
    if city:
        properties = properties.filter(city__icontains=city)
    
    room_type = request.GET.get('room_type')
    if room_type:
        properties = properties.filter(room_type=room_type)
    
    max_price = request.GET.get('price')
    if max_price:
        try:
            properties = properties.filter(monthly_rent__lte=int(max_price))
        except ValueError:
            pass
    
    # Availability filter
    availability = request.GET.get('availability', 'available')
    if availability == 'available':
        properties = properties.filter(available=True)
    elif availability == 'unavailable':
        properties = properties.filter(available=False)
    # if 'all', show all properties
    
    context = {
        'properties': properties,
        'room_types': Property.ROOM_TYPE_CHOICES,
        'availability': availability,
    }
    return render(request, 'index.html', context)


def property_detail(request, id):
    """Display property details with booking functionality"""
    property_obj = get_object_or_404(Property, id=id)
    booking_request = None
    
    if request.user.is_authenticated:
        booking_request = BookingRequest.objects.filter(
            property=property_obj,
            tenant=request.user
        ).first()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to book a property.')
            # Store the return URL with booking section anchor
            request.session['next_page'] = f"{request.get_full_path()}#booking-section"
            return redirect('login')
        
        # Check if user is a tenant (not homeowner)
        try:
            profile = request.user.profile
            if profile.user_type == 'homeowner':
                messages.error(request, 'Home owners cannot book properties.')
                return redirect('property_detail', id=id)
        except UserProfile.DoesNotExist:
            pass
        
        # Check if already booked
        if booking_request and booking_request.status in ['accepted', 'pending']:
            messages.error(request, 'You have already booked this property or a booking request is pending.')
            return redirect('property_detail', id=id)
        
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.property = property_obj
            booking.tenant = request.user
            booking.save()
            messages.success(request, 'Booking request sent! Owner will respond soon.')
            return redirect('property_detail', id=id)
    else:
        form = BookingRequestForm()
    
    context = {
        'property': property_obj,
        'form': form,
        'booking_request': booking_request,
    }
    return render(request, 'property_detail.html', context)


@login_required(login_url='login')
def add_property(request):
    """Add new property (Home owner only)"""
    try:
        profile = request.user.profile
        if profile.user_type != 'homeowner':
            messages.error(request, 'Only home owners can add properties.')
            return redirect('property_list')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('home')
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()
            
            # Handle additional images
            images = request.FILES.getlist('additional_images')
            for image in images:
                PropertyImage.objects.create(property=property_obj, image=image)
            
            messages.success(request, 'Property added successfully!')
            return redirect('property_detail', id=property_obj.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PropertyForm()
    
    return render(request, 'add_property.html', {'form': form})


@login_required(login_url='login')
def edit_property(request, id):
    """Edit property (Home owner only)"""
    property_obj = get_object_or_404(Property, id=id)
    
    if property_obj.owner != request.user:
        messages.error(request, 'You do not have permission to edit this property.')
        return redirect('property_detail', id=id)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('property_detail', id=id)
    else:
        form = PropertyForm(instance=property_obj)
    
    return render(request, 'edit_property.html', {'form': form, 'property': property_obj})


@login_required(login_url='login')
def my_properties(request):
    """List properties owned by home owner"""
    try:
        profile = request.user.profile
        if profile.user_type != 'homeowner':
            messages.error(request, 'Only home owners can access this page.')
            return redirect('property_list')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('home')
    
    properties = request.user.properties.all()
    return render(request, 'my_properties.html', {'properties': properties})


@login_required(login_url='login')
def my_bookings(request):
    """List bookings for logged-in tenant"""
    try:
        profile = request.user.profile
        if profile.user_type != 'user':
            messages.error(request, 'Only tenants can access this page.')
            return redirect('property_list')
    except UserProfile.DoesNotExist:
        pass
    
    bookings = BookingRequest.objects.filter(tenant=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})


@login_required(login_url='login')
def booking_requests(request):
    """List booking requests for home owner's properties"""
    try:
        profile = request.user.profile
        if profile.user_type != 'homeowner':
            messages.error(request, 'Only home owners can access this page.')
            return redirect('property_list')
    except UserProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile first.')
        return redirect('home')
    
    # Get all booking requests for this owner's properties
    booking_requests = BookingRequest.objects.filter(
        property__owner=request.user
    ).order_by('-requested_at')
    
    return render(request, 'booking_requests.html', {'booking_requests': booking_requests})


@login_required(login_url='login')
def respond_to_booking(request, booking_id):
    """Respond to booking request (Accept/Reject)"""
    booking = get_object_or_404(BookingRequest, id=booking_id)
    
    if booking.property.owner != request.user:
        messages.error(request, 'You do not have permission to respond to this booking.')
        return redirect('booking_requests')
    
    if request.method == 'POST':
        form = BookingResponseForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.responded_at = timezone.now()
            booking.save()
            
            # Mark property as unavailable if booking is accepted
            if booking.status == 'accepted':
                booking.property.available = False
                booking.property.save()
            
            status_text = booking.get_status_display()
            messages.success(request, f'Booking request {status_text.lower()}!')
            return redirect('booking_requests')
    else:
        form = BookingResponseForm(instance=booking)
    
    return render(request, 'respond_to_booking.html', {'form': form, 'booking': booking})


def register_user(request):
    """Register as a Tenant"""
    if request.user.is_authenticated:
        return redirect('property_list')
    
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            password = user_form.cleaned_data['password']
            
            # Check if user already exists
            if User.objects.filter(username=user_form.cleaned_data['username']).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register_user')
            
            if User.objects.filter(email=user_form.cleaned_data['email']).exists():
                messages.error(request, 'Email already exists!')
                return redirect('register_user')
            
            # Create user
            user = user_form.save(commit=False)
            user.set_password(password)
            user.save()
            
            # Create profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.user_type = 'user'
            profile.save()
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        else:
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"User: {error}")
            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f"Profile: {error}")
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
    
    return render(request, 'register_user.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


def register_homeowner(request):
    """Register as a Home Owner"""
    if request.user.is_authenticated:
        return redirect('property_list')
    
    if request.method == 'POST':
        user_form = HomeOwnerRegistrationForm(request.POST)
        profile_form = HomeOwnerProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            password = user_form.cleaned_data['password']
            
            # Check if user already exists
            if User.objects.filter(username=user_form.cleaned_data['username']).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register_homeowner')
            
            if User.objects.filter(email=user_form.cleaned_data['email']).exists():
                messages.error(request, 'Email already exists!')
                return redirect('register_homeowner')
            
            # Create user
            user = user_form.save(commit=False)
            user.set_password(password)
            user.save()
            
            # Create profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.user_type = 'homeowner'
            profile.save()
            
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        else:
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"User: {error}")
            for field, errors in profile_form.errors.items():
                for error in errors:
                    messages.error(request, f"Profile: {error}")
    else:
        user_form = HomeOwnerRegistrationForm()
        profile_form = HomeOwnerProfileForm()
    
    return render(request, 'register_homeowner.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


def login_view(request):
    """Login user"""
    if request.user.is_authenticated:
        return redirect('property_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            
            # Redirect to next page if available, else property list
            next_page = request.session.pop('next_page', None)
            if next_page:
                return redirect(next_page)
            return redirect('property_list')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'login.html')


def logout_view(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('property_list')


def forgot_password(request):
    """Password reset request"""
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                
                # Generate password reset token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Create password reset link
                reset_link = f"http://{request.get_host()}/reset-password/{uid}/{token}/"
                
                # Send email
                subject = 'Password Reset Request'
                message = f"""Hi {user.username},

You requested a password reset. Click the link below to reset your password:

{reset_link}

This link will expire in 24 hours.

If you didn't request this, please ignore this email.

Best regards,
The Property Management Team"""
                
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Password reset instructions have been sent to your email. Please check your inbox and spam folder.')
                except Exception as e:
                    print(f"Error sending email: {e}")
                    messages.warning(request, 'Password reset link generated, but email could not be sent. Please check your email configuration.')
                
                return redirect('login')
            except User.DoesNotExist:
                # Don't reveal whether email exists (security best practice)
                messages.success(request, 'If this email exists in our system, you will receive a password reset link shortly.')
                return redirect('login')
    else:
        form = PasswordResetForm()
    
    return render(request, 'forgot_password.html', {'form': form})


def register_choice(request):
    """Show registration type choice"""
    if request.user.is_authenticated:
        return redirect('property_list')
    
    return render(request, 'register_choice.html')

