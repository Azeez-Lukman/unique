from django.db import models


class Enquiry(models.Model):
    CATEGORY_CHOICES = [
        ('construction_residential', 'Residential Construction'),
        ('construction_commercial', 'Commercial Construction'),
        ('property_management', 'Property Management'),
        ('property_sales', 'Property Sales / Sourcing'),
        ('property_rentals', 'Property Rentals / Leasing'),
        ('general', 'General Enquiry'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    category = models.CharField(
        max_length=40,
        choices=CATEGORY_CHOICES,
        default='general'
    )
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_reviewed = models.BooleanField(
        default=False,
        help_text="Check when customer has been contacted"
    )
    staff_notes = models.TextField(
        blank=True,
        help_text="Internal staff notes regarding this enquiry"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Customer Enquiry"
        verbose_name_plural = "Customer Enquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_category_display()} ({self.created_at.strftime('%Y-%m-%d')})"


class Property(models.Model):
    LISTING_TYPE_CHOICES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ]

    PROPERTY_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('land', 'Land / Plot'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPE_CHOICES)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default="USD")
    location = models.CharField(max_length=200)
    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    area_sqft = models.PositiveIntegerField(null=True, blank=True, help_text="Total area (sq ft or sq m)")
    description = models.TextField()
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Property Listing"
        verbose_name_plural = "Property Listings"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_listing_type_display()})"
