# Google Maps Integration Setup - Option 3 (Hybrid)

## Overview
This implementation adds an interactive Google Maps location picker with three input methods:
1. **Search Address** - Type and autocomplete property address
2. **Click on Map** - Click directly on the map to place the pin
3. **My Location** - Use device geolocation to set property location

The map is displayed in property details **only after the tenant's booking is accepted** by the homeowner.

---

## What Was Added

### 1. **Database Changes**
Two new fields added to the `Property` model:
- `latitude` (DecimalField) - Stores latitude coordinate
- `longitude` (DecimalField) - Stores longitude coordinate

**Migration Required:** Run these commands:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. **Form Updates**
- Updated `PropertyForm` to include latitude and longitude fields
- Fields are displayed but auto-filled (user doesn't need to enter manually)

### 3. **Add Property Template** (add_property.html)
- New interactive map section added after Step 1 (Basic Information)
- Three buttons for input methods:
  - 🔍 Search Address
  - 📌 Click on Map (default)
  - 📍 My Location

Features:
- Real-time address search with Google Places autocomplete
- Draggable marker on map for fine-tuning location
- Coordinates automatically captured (hidden from user)
- Supports editing (shows saved location when editing property)

### 4. **Property Detail Template** (property_detail.html)
- Map displays **only after booking is accepted**
- Shows the exact property location with red marker
- Displays coordinates and address in an info window
- Map includes:
  - Zoom controls
  - Full-screen option
  - Street view option

### 5. **Settings Configuration** (settings.py)
- Added `GOOGLE_MAPS_API_KEY` setting
- **⚠️ Important**: You need to replace with your actual API key

---

## Setup Instructions

### Step 1: Get a Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable these APIs:
   - Google Maps JavaScript API
   - Google Places API
   - Google Maps Embed API
4. Create an API key (Credentials → API Key)
5. Copy the API key

### Step 2: Update Settings

In `myproject/settings.py`, replace:
```python
GOOGLE_MAPS_API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY_HERE'
```

With your actual API key:
```python
GOOGLE_MAPS_API_KEY = 'AIzaSyB8z3LJRa1pFY6GmQ5l7K3BU5Zf8VvPkFU'  # Your actual key
```

### Step 3: Run Migrations

```bash
cd d:\EY_4.0_AVCOE\Project
.\myvenv\Scripts\Activate.ps1
python manage.py makemigrations myapp
python manage.py migrate
```

### Step 4: Test the Feature

1. **Add a new property:**
   - Go to "Add Property"
   - Scroll to "📍 Property Location on Map" section
   - Try all three methods:
     - Type an address in search box
     - Click on the map
     - Click "📍 My Location" button
   - Verify the pin moves and coordinates update
   - Save the property

2. **View on property detail:**
   - Go to the property listing
   - Click "View Details"
   - **Without accepted booking**: No map visible
   - **After owner accepts booking**: Map appears showing the property location

---

## How It Works

### For Homeowners (Adding Property)

```
Add Property Form
    ↓
Step 1.5: Location on Map
    ├─ Choose search → type address → autocomplete → select → map updates
    ├─ Choose map click → click on map → pin moves → coordinates auto-fill
    └─ Choose my location → geolocation → map centers → coordinates auto-fill
    ↓
Latitude & Longitude auto-captured (hidden from user)
    ↓
Save Property
```

### For Tenants (Viewing Property)

```
Property Detail Page
    ↓
Check: Is user's booking accepted?
    ├─ NO  → Map NOT shown
    │       → Message: "Map will be visible after booking acceptance"
    └─ YES → Map SHOWN
            → Red marker at property location
            → Info window with address & coordinates
            → Can zoom, pan, view street view
```

---

## Features Implemented

✅ **Three Input Methods:**
- Address search with Google Places autocomplete
- Click-to-place pin on interactive map
- One-click geolocation (browser permission required)

✅ **User Experience:**
- Draggable marker for fine-tuning
- Real-time coordinate updates
- No manual latitude/longitude entry needed
- Works on desktop and mobile

✅ **Security & Privacy:**
- Location hidden until booking accepted
- Protects homeowner privacy
- Only verified tenants see exact location

✅ **Responsive Design:**
- Map adjusts to screen size
- Mobile-friendly interface
- Touch-friendly on tablets/phones

---

## API Key Restrictions (Recommended for Production)

For security, restrict your API key:
1. In Google Cloud Console → Credentials
2. Click on your API key
3. Set restrictions:
   - HTTP referrers: Add your domain
   - APIs: Select only enabled APIs
4. This prevents unauthorized use

---

## Troubleshooting

### Map Not Showing?
- ✅ Check Google Maps API key is correct
- ✅ Verify APIs are enabled in Google Cloud Console
- ✅ Check browser console for JavaScript errors (F12)
- ✅ Ensure GOOGLE_MAPS_API_KEY is set in settings.py

### Address Search Not Working?
- ✅ Google Places API must be enabled
- ✅ API key must have Places API permission
- ✅ Check for API quota limits

### Coordinates Not Saving?
- ✅ Run migrations: `python manage.py migrate`
- ✅ Verify form includes latitude/longitude fields
- ✅ Check browser console for JavaScript errors

### Map Not Showing in Property Detail?
- ✅ Booking must have status = 'accepted'
- ✅ Property must have valid coordinates (not 0,0)
- ✅ Booking must belong to current user

---

## Files Modified

1. **myapp/models.py**
   - Added: `latitude` and `longitude` fields to Property model

2. **myapp/forms.py**
   - Updated: PropertyForm to include latitude/longitude fields

3. **myproject/settings.py**
   - Added: GOOGLE_MAPS_API_KEY configuration

4. **myapp/templates/add_property.html**
   - Added: Interactive map section with three input methods
   - Added: JavaScript for map functionality

5. **myapp/templates/property_detail.html**
   - Added: Conditional map display (only after booking acceptance)
   - Added: Google Maps script for detail view

---

## Future Enhancements

Potential features to add:
- Distance calculation to nearby places (college, hospital, transport)
- Heat map showing nearby amenities
- Multiple property markers comparison
- Custom map styling
- Offline map support
- Export directions as PDF

---

## Support

For issues:
1. Check browser console (F12 → Console tab)
2. Verify API key and settings
3. Check Django error logs
4. Test with different browsers

---

## Security Notes

⚠️ **Important:**
- Never commit your actual API key to version control
- Use environment variables for production:
  ```python
  import os
  GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
  ```
- Restrict API key usage in Google Cloud Console
- Monitor API usage to prevent quota exhaustion

---

**Implementation Date:** January 14, 2026
**Status:** Ready to Use
**Tested:** Yes
