# Smart Rental Home - API Endpoints Reference

## Authentication Endpoints

### 1. User Registration - Choose Type
- **URL**: `/register/`
- **Method**: GET
- **Auth Required**: No
- **Description**: Shows choice between tenant and home owner registration
- **Template**: register_choice.html

### 2. Register as Tenant
- **URL**: `/register/user/`
- **Method**: GET, POST
- **Auth Required**: No
- **Parameters**:
  - first_name (text)
  - last_name (text)
  - username (text, unique)
  - email (email, unique)
  - password (password)
  - password_confirm (password)
  - phone (text, optional)
  - village (text, optional)
  - subdistrict (text, optional)
  - district (text, optional)
- **Response**: Redirects to login on success
- **Template**: register_user.html

### 3. Register as Home Owner
- **URL**: `/register/homeowner/`
- **Method**: GET, POST
- **Auth Required**: No
- **Parameters**:
  - first_name (text)
  - last_name (text)
  - username (text, unique)
  - email (email, unique)
  - password (password)
  - password_confirm (password)
  - phone (text, optional)
- **Response**: Redirects to login on success
- **Template**: register_homeowner.html

### 4. Login
- **URL**: `/login/`
- **Method**: GET, POST
- **Auth Required**: No
- **Parameters**:
  - username (text, required)
  - password (password, required)
- **Response**: Redirects to property list or next_page from session
- **Template**: login.html
- **Features**: 
  - Stores next_page in session for redirect after login
  - Shows "Forgot Password?" link

### 5. Logout
- **URL**: `/logout/`
- **Method**: GET
- **Auth Required**: Yes
- **Response**: Redirects to property list with success message
- **Status Code**: 302 (Redirect)

### 6. Forgot Password
- **URL**: `/forgot-password/`
- **Method**: GET, POST
- **Auth Required**: No
- **Parameters**:
  - email (email, required)
- **Response**: Redirects to login on success
- **Template**: forgot_password.html
- **Note**: Currently shows message. In production, sends reset email.

---

## Property Endpoints

### 7. Property List (Search)
- **URL**: `/`
- **Method**: GET
- **Auth Required**: No
- **Query Parameters**:
  - city (optional) - Filter by city name
  - room_type (optional) - Filter by room type
  - price (optional) - Filter by max price
- **Response**: HTML page with property grid
- **Template**: index.html
- **Features**: 
  - Shows only available properties
  - Property cards with image, price, location
  - Search filters for city, room type, price

### 8. Property Detail
- **URL**: `/property/<int:id>/`
- **Method**: GET, POST
- **Auth Required**: No (GET), Yes (POST)
- **POST Parameters**:
  - message (textarea, optional) - Message to property owner
- **Response**: 
  - GET: HTML page with full property details and booking sidebar
  - POST: Redirects to same property or login
- **Template**: property_detail.html
- **Features**:
  - Shows all 10 property sections
  - Displays amenities as badges
  - Shows booking status if user has requested
  - Booking form if authenticated tenant
  - Price summary sidebar
  - Property images gallery

### 9. Add Property
- **URL**: `/add-property/`
- **Method**: GET, POST
- **Auth Required**: Yes (home owner only)
- **POST Parameters**:
  - title (text) - Room title
  - room_type (select) - Room type
  - flat_system (select) - Flat system
  - city (text) - City name
  - area_location (text) - Area/Location
  - full_address (textarea) - Full address
  - monthly_rent (number) - Monthly rent
  - security_deposit (number) - Security deposit
  - maintenance_charges (number) - Maintenance charges
  - max_people (number) - Maximum people
  - per_person_rent (number) - Per person rent
  - main_image (file) - Main room image
  - additional_images (file multiple) - Additional images
  - floor_number (number) - Floor number
  - total_floors (number) - Total floors
  - furnishing_status (select) - Furnishing status
  - amenities (checkbox multiple) - Amenities
  - nearby_college_office (text) - Nearby college/office
  - nearby_mall (text) - Nearby mall
  - garden_park_nearby (text) - Garden/park nearby
  - hospital_medical (text) - Hospital/medical store
  - temple_religious (text) - Temple/religious place
  - bus_railway_distance (text) - Bus/railway distance
  - mess_available (checkbox) - Mess available
  - mess_type (select) - Mess type
  - mess_distance (text) - Mess distance
  - tiffin_available (checkbox) - Tiffin available
  - preferred_tenant_type (select) - Preferred tenant type
  - gender_preference (select) - Gender preference
  - smoking_allowed (checkbox) - Smoking allowed
  - drinking_allowed (checkbox) - Drinking allowed
  - pets_allowed (checkbox) - Pets allowed
  - available_from (date) - Available from date
  - min_stay_duration (number) - Minimum stay duration
  - description (textarea) - Room description
- **Response**: Redirects to property detail on success
- **Template**: add_property.html
- **Permission**: Home owner only

### 10. Edit Property
- **URL**: `/edit-property/<int:id>/`
- **Method**: GET, POST
- **Auth Required**: Yes (home owner only, property owner)
- **POST Parameters**: Same as add-property
- **Response**: Redirects to property detail on success
- **Template**: edit_property.html
- **Permission**: Property owner only

### 11. My Properties
- **URL**: `/my-properties/`
- **Method**: GET
- **Auth Required**: Yes (home owner only)
- **Response**: HTML page with list of properties
- **Template**: my_properties.html
- **Features**:
  - Shows all properties owned by home owner
  - Displays property image, location, rent
  - Shows availability status
  - Shows count of booking requests
  - Action buttons: View, Edit, View Requests

---

## Booking Endpoints

### 12. My Bookings (Tenant)
- **URL**: `/my-bookings/`
- **Method**: GET
- **Auth Required**: Yes (tenant only)
- **Response**: HTML page with list of booking requests
- **Template**: my_bookings.html
- **Features**:
  - Shows all bookings made by tenant
  - Displays status badges
  - Shows status-specific messages
  - Links to property details

### 13. Booking Requests (Home Owner)
- **URL**: `/booking-requests/`
- **Method**: GET
- **Auth Required**: Yes (home owner only)
- **Query Parameters**:
  - property (optional) - Filter by property ID
- **Response**: HTML page with table of booking requests
- **Template**: booking_requests.html
- **Features**:
  - Shows all requests for owner's properties
  - Displays tenant info, property, request date
  - Shows current status
  - Action button to respond

### 14. Respond to Booking
- **URL**: `/respond-booking/<int:booking_id>/`
- **Method**: GET, POST
- **Auth Required**: Yes (property owner only)
- **POST Parameters**:
  - status (select) - 'pending', 'accepted', 'rejected', 'cancelled'
  - owner_response (textarea) - Message to tenant
- **Response**: Redirects to booking requests on success
- **Template**: respond_to_booking.html
- **Features**:
  - Shows tenant information
  - Shows property details
  - Shows tenant's message
  - Decision form if pending
  - Read-only view if already responded

---

## Informational Endpoints

### 15. About
- **URL**: `/about/`
- **Method**: GET
- **Auth Required**: No
- **Response**: HTML page with about information
- **Template**: about.html

---

## Response Codes Reference

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 302 | Redirect - After form submission |
| 403 | Forbidden - User not authorized |
| 404 | Not Found - Resource doesn't exist |
| 500 | Server Error |

---

## Error Messages

| Error | Condition |
|-------|-----------|
| Passwords do not match | Password confirmation doesn't match |
| Username already exists | Username taken |
| Email already exists | Email already registered |
| Please login to book | Non-authenticated user tries to book |
| Only home owners can add properties | User tries to add property as tenant |
| You do not have permission | Trying to edit someone else's property |
| Only tenants can access this page | Home owner tries to access My Bookings |
| Only home owners can access this page | Tenant tries to access Booking Requests |

---

## Session Management

- **next_page**: Stored in session when user redirects to login
- **Redirect Logic**: After successful login, user is redirected to next_page if available
- **Default Redirect**: Property list if no next_page

---

## Filtering & Search

### Property List Search
```
GET / ?city=Mumbai&room_type=1bhk&price=15000
```
- city: Case-insensitive substring match
- room_type: Exact match against choices
- price: Properties with monthly_rent <= price

### Booking Requests Filter
```
GET /booking-requests/?property=5
```
- property: Show requests for specific property

---

## Form Validation

### Username
- Unique
- Required
- Text format

### Email
- Unique
- Required
- Valid email format

### Password
- Required
- Must match confirmation
- Stored as hash

### Phone
- Optional
- Text format

### Numeric Fields (Rent, Deposit, People)
- Required
- Must be positive number
- Server-side validation

### Date Fields
- Required
- Date format (YYYY-MM-DD)
- Must be valid date

### Textarea Fields
- Optional
- Text format
- No length limit

### File Upload
- Images only (main_image required, additional optional)
- Multiple allowed for additional_images
- Stored in media/property_images/

---

## JSON Data Structures

### Amenities
```json
["bed", "mattress", "wardrobe", "study_table", "wifi", "fan", "ac", "geyser"]
```
- Stored as JSON string in database
- Parsed to list on retrieval
- Available options: bed, mattress, wardrobe, study_table, wifi, fan, ac, geyser, washing_machine, refrigerator, parking, lift

---

## Permission Matrix

| Endpoint | Guest | Tenant | Home Owner |
|----------|-------|--------|-----------|
| /register/ | ✓ | ✗ | ✗ |
| /login/ | ✓ | ✗ | ✗ |
| /logout/ | ✗ | ✓ | ✓ |
| / | ✓ | ✓ | ✓ |
| /property/<id>/ (GET) | ✓ | ✓ | ✓ |
| /property/<id>/ (POST) | ✗ | ✓ | ✗ |
| /add-property/ | ✗ | ✗ | ✓ |
| /edit-property/<id>/ | ✗ | ✗ | ✓* |
| /my-properties/ | ✗ | ✗ | ✓ |
| /my-bookings/ | ✗ | ✓ | ✗ |
| /booking-requests/ | ✗ | ✗ | ✓ |
| /respond-booking/<id>/ | ✗ | ✗ | ✓* |

*Owner of resource only

---

## Testing Commands

```bash
# User registration (Tenant)
POST /register/user/
username=tenant1&email=tenant@example.com&password=Pass123&password_confirm=Pass123

# User registration (Home Owner)
POST /register/homeowner/
username=owner1&email=owner@example.com&password=Pass123&password_confirm=Pass123

# Login
POST /login/
username=tenant1&password=Pass123

# Add Property
POST /add-property/
[Form with all fields]

# Create Booking
POST /property/1/
message=Interested in this property

# Respond Booking
POST /respond-booking/1/
status=accepted&owner_response=Welcome!
```

---

For implementation details, see SYSTEM_UPDATES.md
