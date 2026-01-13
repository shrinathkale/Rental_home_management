from django.urls import path
from . import views

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('about/', views.about, name='about'),
    path('property/<int:id>/', views.property_detail, name='property_detail'),
    path('add-property/', views.add_property, name='add_property'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
