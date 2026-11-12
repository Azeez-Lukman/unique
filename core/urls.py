from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Public Website Routes
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('construction/', views.construction, name='construction'),
    path('real-estate/', views.real_estate, name='real_estate'),
    path('properties/', views.properties, name='properties'),
    path('contact/', views.contact, name='contact'),

    # Staff Operations Dashboard
    path('dashboard/login/', views.dashboard_login, name='dashboard_login'),
    path('dashboard/logout/', views.dashboard_logout, name='dashboard_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/properties/', views.dashboard_properties, name='dashboard_properties'),
    path('dashboard/enquiry/<int:enquiry_id>/toggle/', views.toggle_enquiry_status, name='toggle_enquiry_status'),
    path('dashboard/export-csv/', views.export_enquiries_csv, name='export_enquiries_csv'),
]
