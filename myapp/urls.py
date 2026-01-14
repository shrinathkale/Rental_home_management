from django.urls import path
from . import views

urlpatterns = [
    # Properties
    path('', views.property_list, name='property_list'),
    path('property/<int:id>/', views.property_detail, name='property_detail'),
    path('add-property/', views.add_property, name='add_property'),
    path('edit-property/<int:id>/', views.edit_property, name='edit_property'),
    path('my-properties/', views.my_properties, name='my_properties'),
    path('toggle-property-availability/<int:id>/', views.toggle_property_availability, name='toggle_property_availability'),
    
    # Booking
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking-requests/', views.booking_requests, name='booking_requests'),
    path('respond-booking/<int:booking_id>/', views.respond_to_booking, name='respond_to_booking'),
    
    # Authentication
    path('about/', views.about, name='about'),
    path('register/', views.register_choice, name='register_choice'),
    path('register/user/', views.register_user, name='register_user'),
    path('register/homeowner/', views.register_homeowner, name='register_homeowner'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]

