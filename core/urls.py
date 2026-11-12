from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('construction/', views.construction, name='construction'),
    path('real-estate/', views.real_estate, name='real_estate'),
    path('properties/', views.properties, name='properties'),
    path('contact/', views.contact, name='contact'),
]

