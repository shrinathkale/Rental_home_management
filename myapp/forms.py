from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Property, BookingRequest, PropertyImage
import json


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password_confirm'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'village', 'subdistrict', 'district']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'village': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Village'}),
            'subdistrict': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sub-district'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'District'}),
        }


class HomeOwnerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password_confirm'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data


class HomeOwnerProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }


class PropertyForm(forms.ModelForm):
    AMENITIES_CHOICES = [
        ('bed', 'Bed'),
        ('mattress', 'Mattress'),
        ('wardrobe', 'Wardrobe'),
        ('study_table', 'Study Table'),
        ('wifi', 'Wi-Fi'),
        ('fan', 'Fan'),
        ('ac', 'AC'),
        ('geyser', 'Geyser'),
        ('washing_machine', 'Washing Machine'),
        ('refrigerator', 'Refrigerator'),
        ('parking', 'Parking'),
        ('lift', 'Lift'),
    ]
    
    amenities = forms.MultipleChoiceField(
        choices=AMENITIES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Amenities'
    )
    
    class Meta:
        model = Property
        fields = [
            'title', 'room_type', 'flat_system', 'city', 'area_location', 'full_address',
            'monthly_rent', 'security_deposit', 'maintenance_charges', 'max_people', 'per_person_rent',
            'main_image', 'floor_number', 'total_floors', 'furnishing_status',
            'latitude', 'longitude',
            'nearby_college_office', 'nearby_mall', 'garden_park_nearby', 'hospital_medical',
            'temple_religious', 'bus_railway_distance', 'mess_available', 'mess_type',
            'mess_distance', 'tiffin_available', 'preferred_tenant_type', 'gender_preference',
            'smoking_allowed', 'drinking_allowed', 'pets_allowed', 'available_from',
            'min_stay_duration', 'description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Room Title'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'flat_system': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location/Area'}),
            'area_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'full_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}),
            'monthly_rent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly Rent'}),
            'security_deposit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Security Deposit'}),
            'maintenance_charges': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Maintenance Charges'}),
            'max_people': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max People Allowed'}),
            'per_person_rent': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Per Person Rent'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
            'floor_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Floor Number'}),
            'total_floors': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Floors'}),
            'furnishing_status': forms.Select(attrs={'class': 'form-control'}),
            'nearby_college_office': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nearby College/Office'}),
            'nearby_mall': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nearby Mall'}),
            'garden_park_nearby': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Garden/Park Nearby'}),
            'hospital_medical': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hospital/Medical Store'}),
            'temple_religious': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Temple/Religious Place'}),
            'bus_railway_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bus Stop/Railway Distance'}),
            'mess_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'mess_type': forms.Select(attrs={'class': 'form-control'}),
            'mess_distance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mess Distance'}),
            'tiffin_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'preferred_tenant_type': forms.Select(attrs={'class': 'form-control'}),
            'gender_preference': forms.Select(attrs={'class': 'form-control'}),
            'smoking_allowed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'drinking_allowed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pets_allowed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'available_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'min_stay_duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimum Stay (Months)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Room Description'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.amenities:
            try:
                amenities_list = json.loads(self.instance.amenities) if isinstance(self.instance.amenities, str) else self.instance.amenities
                self.fields['amenities'].initial = amenities_list
            except:
                pass
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        amenities = self.cleaned_data.get('amenities')
        instance.amenities = json.dumps(amenities) if amenities else '[]'
        if commit:
            instance.save()
        return instance


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class BookingRequestForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell property owner about yourself (optional)'}),
        }


class BookingResponseForm(forms.ModelForm):
    class Meta:
        model = BookingRequest
        fields = ['status', 'owner_response']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'owner_response': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your response to tenant'}),
        }


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )
