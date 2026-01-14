from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('user', 'Tenant'),
        ('homeowner', 'Home Owner'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # User-specific fields
    village = models.CharField(max_length=100, blank=True, null=True)
    subdistrict = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"


class Property(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Single Room'),
        ('shared', 'Shared Room'),
        ('1bhk', '1 BHK'),
        ('2bhk', '2 BHK'),
        ('pg', 'PG Room'),
    ]
    
    FLAT_SYSTEM_CHOICES = [
        ('entire', 'Entire Flat'),
        ('room', 'Only Room'),
        ('pg', 'PG System'),
    ]
    
    FURNISHING_CHOICES = [
        ('fully', 'Fully Furnished'),
        ('semi', 'Semi Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    
    MESS_TYPE_CHOICES = [
        ('veg', 'Veg'),
        ('nonveg', 'Non-Veg'),
        ('both', 'Both'),
    ]
    
    TENANT_TYPE_CHOICES = [
        ('students', 'Students'),
        ('professionals', 'Working Professionals'),
        ('family', 'Family'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('any', 'Any'),
    ]
    
    # Basic Information
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES)
    flat_system = models.CharField(max_length=50, choices=FLAT_SYSTEM_CHOICES)
    city = models.CharField(max_length=100, default='')
    area_location = models.CharField(max_length=200, default='')
    full_address = models.TextField(default='')
    
    # Pricing & Capacity
    monthly_rent = models.IntegerField(validators=[MinValueValidator(0)])
    security_deposit = models.IntegerField(validators=[MinValueValidator(0)])
    maintenance_charges = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    max_people = models.IntegerField(validators=[MinValueValidator(1)])
    per_person_rent = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    
    # Images
    main_image = models.ImageField(upload_to="property_images/")
    
    # Room Details
    floor_number = models.IntegerField(validators=[MinValueValidator(0)])
    total_floors = models.IntegerField(validators=[MinValueValidator(1)])
    furnishing_status = models.CharField(max_length=50, choices=FURNISHING_CHOICES)
    
    # Amenities (comma-separated or use through model)
    amenities = models.TextField(blank=True, null=True)  # JSON format
    
    # Location Coordinates (for Google Maps)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, help_text="Property latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0, help_text="Property longitude")
    
    # Nearby Places
    nearby_college_office = models.CharField(max_length=200, blank=True, null=True)
    nearby_mall = models.CharField(max_length=200, blank=True, null=True)
    garden_park_nearby = models.CharField(max_length=200, blank=True, null=True)
    hospital_medical = models.CharField(max_length=200, blank=True, null=True)
    temple_religious = models.CharField(max_length=200, blank=True, null=True)
    bus_railway_distance = models.CharField(max_length=200, blank=True, null=True)
    
    # Food & Mess
    mess_available = models.BooleanField(default=False)
    mess_type = models.CharField(max_length=50, choices=MESS_TYPE_CHOICES, blank=True, null=True)
    mess_distance = models.CharField(max_length=200, blank=True, null=True)
    tiffin_available = models.BooleanField(default=False)
    
    # Rules & Preferences
    preferred_tenant_type = models.CharField(max_length=100, choices=TENANT_TYPE_CHOICES)
    gender_preference = models.CharField(max_length=50, choices=GENDER_CHOICES)
    smoking_allowed = models.BooleanField(default=False)
    drinking_allowed = models.BooleanField(default=False)
    pets_allowed = models.BooleanField(default=False)
    
    # Availability
    available_from = models.DateField(default='2024-01-01')
    min_stay_duration = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    
    # Description
    description = models.TextField()
    
    # Status
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    @property
    def amenities_list(self):
        """Convert JSON amenities string to list"""
        if self.amenities:
            try:
                import json
                if isinstance(self.amenities, str):
                    return json.loads(self.amenities)
                return self.amenities
            except:
                return []
        return []
    
    class Meta:
        ordering = ['-created_at']


class BookingRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='booking_requests')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booking_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, null=True)
    owner_response = models.TextField(blank=True, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Booking Request: {self.property.title} by {self.tenant.username}"
    
    class Meta:
        ordering = ['-requested_at']
        unique_together = ['property', 'tenant']


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to="property_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"
