# Smart Rental Home - Setup & User Guide

## Quick Start

### 1. Environment Setup
```bash
# Activate virtual environment
.\myvenv\Scripts\Activate.ps1

# The server should be running on http://127.0.0.1:8000
```

### 2. Database
- MySQL database: `homes`
- Tables automatically created via migrations
- All new models: UserProfile, BookingRequest, PropertyImage

### 3. Admin Panel
- Access: http://127.0.0.1:8000/admin/
- All models are registered in admin.py

## User Workflows

### Workflow 1: Tenant Registration & Booking

1. **Register as Tenant**
   - Go to http://127.0.0.1:8000/register/
   - Click "Register as Tenant"
   - Fill in all fields including Village, Sub-district, District
   - Submit

2. **Login**
   - Go to http://127.0.0.1:8000/login/
   - Enter username and password
   - Click Login

3. **Browse Properties**
   - Homepage shows all available properties
   - Use search filters: City, Room Type, Max Price
   - Click "View Details" on any property

4. **Book Property**
   - On property detail page, scroll to right sidebar
   - If logged in as tenant: Fill message (optional) and click "Send Booking Request"
   - If not logged in: Click "Login to Book"
   - System stores your session and redirects after login

5. **Track Bookings**
   - Click "My Bookings" in navigation
   - See all your booking requests
   - Check status: Pending/Accepted/Rejected
   - View owner's message

### Workflow 2: Home Owner Registration & Listing

1. **Register as Home Owner**
   - Go to http://127.0.0.1:8000/register/
   - Click "Register as Home Owner"
   - Fill in account details
   - Submit

2. **Login**
   - Go to http://127.0.0.1:8000/login/
   - Enter credentials
   - You'll see "Add Property" in navigation bar

3. **Add Property**
   - Click "Add Property" in navigation
   - Fill in all 10 sections:
     - Basic Room Info
     - Pricing & Capacity
     - Images (main + additional)
     - Room Details
     - Amenities (checkboxes)
     - Nearby Places
     - Food & Mess
     - Rules & Preferences
     - Availability
     - Description
   - Click "Add Property"

4. **Manage Properties**
   - Click "My Properties" in navigation
   - See all your listed properties
   - View booking count
   - Edit or view details

5. **Respond to Bookings**
   - Click "Booking Requests" in navigation
   - See all requests for your properties
   - Click "Respond" to accept/reject
   - Add optional message to tenant
   - Submit response

6. **Property Status**
   - "Available" badge shows properties accepting bookings
   - "Booked" badge shows unavailable properties
   - Track all booking requests in one place

## Navigation Bar Changes

### Before Login
- Home | About | Login | Register

### After Login (Tenant)
- Home | About | My Bookings | Welcome, [username] | Logout

### After Login (Home Owner)
- Home | About | Add Property | My Properties | Booking Requests | Welcome, [username] | Logout

## Password Reset

1. Go to http://127.0.0.1:8000/login/
2. Click "Forgot Password?"
3. Enter your email address
4. In production, email with reset link will be sent
5. Currently shows confirmation message

## Property Search Features

- **City Filter**: Search by city name
- **Room Type Filter**: Single, Shared, 1BHK, 2BHK, PG Room
- **Price Filter**: Search properties below max price

## Booking Status Indicators

| Status | Color | Meaning |
|--------|-------|---------|
| Pending | Yellow | Waiting for owner response |
| Accepted | Green | Owner approved your booking |
| Rejected | Red | Owner declined your request |
| Cancelled | Gray | Booking was cancelled |

## Important Notes

1. **User Types**: The system distinguishes between Users (tenants) and HomeOwners
2. **Session Management**: After login, users are redirected to their last viewed page
3. **In-System Communication**: All booking communications happen within the system (no external emails required for basic functionality)
4. **Location Fields**: Only tenants need to fill Village/SubDistrict/District
5. **Image Management**: Properties support multiple images (1 main + multiple additional)
6. **JSON Storage**: Amenities are stored as JSON for flexible selection

## Key Features Summary

✅ Separate registration for users and home owners  
✅ User location tracking (village, subdistrict, district)  
✅ Comprehensive property listing with 10 sections  
✅ Advanced amenities selection  
✅ Multiple property images  
✅ In-system booking request system  
✅ Accept/Reject booking management  
✅ Owner response messages  
✅ Visible booking status  
✅ Smart login redirects  
✅ Password reset functionality  
✅ Role-based navigation menu  

## Troubleshooting

**Issue**: "Add Property" button not visible
- **Solution**: You must be logged in as a Home Owner. Check your user type in admin or database.

**Issue**: Cannot complete booking
- **Solution**: You must be logged in as a Tenant. Tenants cannot book properties.

**Issue**: Cannot see other properties' bookings
- **Solution**: You can only see booking requests for YOUR properties.

**Issue**: Property detail page not loading
- **Solution**: Check that main_image file exists or upload a new image.

## Database Fields Reference

### User Profile
- user_type: 'user' (tenant) or 'homeowner'
- phone, village, subdistrict, district

### Property (10 Sections)
1. Basic: title, room_type, flat_system, city, area_location, full_address
2. Pricing: monthly_rent, security_deposit, maintenance_charges, max_people, per_person_rent
3. Images: main_image, additional_images (PropertyImage model)
4. Details: floor_number, total_floors, furnishing_status
5. Amenities: amenities (JSON array)
6. Nearby: nearby_college, nearby_mall, garden_park, hospital, temple, bus_railway
7. Mess: mess_available, mess_type, mess_distance, tiffin_available
8. Rules: preferred_tenant_type, gender_preference, smoking, drinking, pets
9. Availability: available_from, min_stay_duration
10. Description: description text

### Booking Request
- property, tenant, status, message, owner_response, requested_at, responded_at

---

For more details, see SYSTEM_UPDATES.md
