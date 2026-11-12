from django.contrib import admin
from .models import Enquiry, Property


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'email', 'phone', 'is_reviewed', 'created_at')
    list_filter = ('category', 'is_reviewed', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message', 'subject')
    list_editable = ('is_reviewed',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Customer Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Enquiry Details', {
            'fields': ('category', 'subject', 'message', 'created_at')
        }),
        ('Management & Follow-up', {
            'fields': ('is_reviewed', 'staff_notes')
        }),
    )


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'listing_type', 'property_type', 'price', 'currency', 'location', 'is_available', 'is_featured')
    list_filter = ('listing_type', 'property_type', 'is_available', 'is_featured')
    search_fields = ('title', 'location', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_available', 'is_featured')
