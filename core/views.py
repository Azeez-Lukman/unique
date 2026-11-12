import logging
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Enquiry, Property
from .forms import EnquiryForm

logger = logging.getLogger(__name__)


def robots_txt(request):
    """Serves clean robots.txt for search engines."""
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def home(request):
    """Homepage view showcasing dual divisions, values, process, and enquiry capture."""
    featured_properties = Property.objects.filter(is_available=True, is_featured=True)[:3]
    
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            _send_enquiry_notification(enquiry)
            messages.success(request, "Thank you! Your enquiry has been received. Our team will contact you shortly.")
            return redirect('core:home')
        else:
            messages.error(request, "Please check the form fields and correct the highlighted errors.")
    else:
        form = EnquiryForm()

    context = {
        'form': form,
        'featured_properties': featured_properties,
    }
    return render(request, 'core/index.html', context)


def about(request):
    """About Us view introducing the company mission, values, and leadership standards."""
    return render(request, 'core/about.html')


def construction(request):
    """Construction services breakdown: residential builds, commercial developments, and process."""
    return render(request, 'core/construction.html')


def real_estate(request):
    """Real estate & property management services view."""
    return render(request, 'core/real_estate.html')


def properties(request):
    """Property showcase for sales and rentals, plus property sourcing requests."""
    listing_type = request.GET.get('type')
    property_type = request.GET.get('property_type')

    listings = Property.objects.filter(is_available=True)
    if listing_type:
        listings = listings.filter(listing_type=listing_type)
    if property_type:
        listings = listings.filter(property_type=property_type)

    context = {
        'listings': listings,
        'selected_type': listing_type,
        'selected_property_type': property_type,
    }
    return render(request, 'core/properties.html', context)


def contact(request):
    """Contact page view with full interactive multi-category enquiry form."""
    initial_category = request.GET.get('category', 'general')
    
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            _send_enquiry_notification(enquiry)
            messages.success(request, "Your message has been sent successfully! We will get in touch with you shortly.")
            return redirect('core:contact')
        else:
            messages.error(request, "There was an issue submitting your enquiry. Please verify the information provided.")
    else:
        form = EnquiryForm(initial={'category': initial_category})

    return render(request, 'core/contact.html', {'form': form})


def _send_enquiry_notification(enquiry):
    """Safely dispatches email notification to company administrators without failing form submission."""
    subject = f"New Enquiry: {enquiry.get_category_display()} - {enquiry.name}"
    message = (
        f"You have received a new enquiry through the website:\n\n"
        f"Name: {enquiry.name}\n"
        f"Email: {enquiry.email}\n"
        f"Phone: {enquiry.phone}\n"
        f"Category: {enquiry.get_category_display()}\n"
        f"Subject: {enquiry.subject or 'N/A'}\n\n"
        f"Message:\n{enquiry.message}\n\n"
        f"Submitted at: {enquiry.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
    )
    recipient = getattr(settings, 'NOTIFICATION_RECIPIENT_EMAIL', 'info@uniqueproperty.com')
    sender = getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@uniqueproperty.com')

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=sender,
            recipient_list=[recipient],
            fail_silently=True
        )
    except Exception as e:
        logger.warning(f"Could not send email notification: {e}")


# ==========================================
# STAFF & MANAGEMENT DASHBOARD
# ==========================================
import csv
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404


def dashboard_login(request):
    """Branded staff portal authentication view."""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect('core:dashboard')
            else:
                messages.error(request, "Access restricted. Staff authorization required.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'dashboard/login.html', {'form': form})


def dashboard_logout(request):
    """Logs staff member out safely."""
    logout(request)
    messages.info(request, "You have been logged out of the staff management portal.")
    return redirect('core:dashboard_login')


@login_required(login_url='core:dashboard_login')
@user_passes_test(lambda u: u.is_staff, login_url='core:dashboard_login')
def dashboard(request):
    """Staff Operations Dashboard with lead pipeline and statistics."""
    current_status = request.GET.get('status')
    current_category = request.GET.get('category')

    enquiries_qs = Enquiry.objects.all()

    # Filter by review status or category
    if current_status == 'pending':
        enquiries_qs = enquiries_qs.filter(is_reviewed=False)
    elif current_status == 'reviewed':
        enquiries_qs = enquiries_qs.filter(is_reviewed=True)

    if current_category:
        enquiries_qs = enquiries_qs.filter(category=current_category)

    # KPI Statistics
    total_count = Enquiry.objects.count()
    pending_count = Enquiry.objects.filter(is_reviewed=False).count()
    construction_count = Enquiry.objects.filter(category__startswith='construction').count()
    real_estate_count = Enquiry.objects.filter(category__startswith='property').count()

    context = {
        'enquiries': enquiries_qs[:50],
        'total_count': total_count,
        'pending_count': pending_count,
        'construction_count': construction_count,
        'real_estate_count': real_estate_count,
        'current_status': current_status,
        'current_category': current_category,
    }
    return render(request, 'dashboard/index.html', context)


@login_required(login_url='core:dashboard_login')
@user_passes_test(lambda u: u.is_staff, login_url='core:dashboard_login')
def dashboard_properties(request):
    """Staff property listings inventory overview."""
    properties = Property.objects.all()
    return render(request, 'dashboard/properties.html', {'properties': properties})


@login_required(login_url='core:dashboard_login')
@user_passes_test(lambda u: u.is_staff, login_url='core:dashboard_login')
def toggle_enquiry_status(request, enquiry_id):
    """Allows staff to toggle an enquiry's reviewed/contacted status with 1 click."""
    if request.method == 'POST':
        enquiry = get_object_or_404(Enquiry, id=enquiry_id)
        enquiry.is_reviewed = not enquiry.is_reviewed
        enquiry.save()
        status_label = "Contacted / Reviewed" if enquiry.is_reviewed else "Pending"
        messages.success(request, f"Enquiry for {enquiry.name} marked as {status_label}.")
    return redirect('core:dashboard')


@login_required(login_url='core:dashboard_login')
@user_passes_test(lambda u: u.is_staff, login_url='core:dashboard_login')
def export_enquiries_csv(request):
    """Exports customer enquiry data into a structured CSV file for spreadsheets."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="unique_customer_enquiries.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Email', 'Phone', 'Category', 'Subject', 'Message', 'Contacted Status', 'Submitted Date'])

    for e in Enquiry.objects.all().order_by('-created_at'):
        writer.writerow([
            e.id,
            e.name,
            e.email,
            e.phone,
            e.get_category_display(),
            e.subject,
            e.message.replace('\n', ' '),
            'Reviewed' if e.is_reviewed else 'Pending',
            e.created_at.strftime('%Y-%m-%d %H:%M')
        ])

    return response
