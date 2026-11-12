from django.test import TestCase, Client
from django.urls import reverse
from .models import Enquiry, Property


class WebsitePagesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_status_and_template(self):
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertContains(response, 'UNIQUE')
        self.assertContains(response, 'Property and Construction')
        self.assertContains(response, 'If you can dream it, we can build it')

    def test_about_page_status_and_template(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about.html')
        self.assertContains(response, 'Our Core Values')

    def test_construction_page_status_and_template(self):
        response = self.client.get(reverse('core:construction'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/construction.html')
        self.assertContains(response, 'Custom Residential Homes')
        self.assertContains(response, 'Commercial Facilities')

    def test_real_estate_page_status_and_template(self):
        response = self.client.get(reverse('core:real_estate'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/real_estate.html')
        self.assertContains(response, 'Property Management')

    def test_properties_page_status_and_template(self):
        response = self.client.get(reverse('core:properties'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/properties.html')
        self.assertContains(response, 'Property Sourcing')

    def test_contact_page_status_and_template(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contact.html')
        self.assertContains(response, 'Send Us a Direct Message')

    def test_sitemap_xml_returns_200(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertContains(response, '<loc>')

    def test_robots_txt_returns_200(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertContains(response, 'User-agent: *')
        self.assertContains(response, 'Disallow: /admin/')
        self.assertContains(response, 'Sitemap:')


class EnquiryFormSubmissionTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_successful_enquiry_submission_via_contact_page(self):
        initial_count = Enquiry.objects.count()
        payload = {
            'name': 'Sarah Jenkins',
            'email': 'sarah@example.com',
            'phone': '+1 (555) 234-5678',
            'category': 'construction_residential',
            'subject': 'New 4-Bedroom Villa Construction',
            'message': 'We have purchased a plot and would like to review design plans and pricing.'
        }
        response = self.client.post(reverse('core:contact'), data=payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Enquiry.objects.count(), initial_count + 1)
        
        enquiry = Enquiry.objects.first()
        self.assertEqual(enquiry.name, 'Sarah Jenkins')
        self.assertEqual(enquiry.category, 'construction_residential')
        self.assertContains(response, 'Your message has been sent successfully')

    def test_successful_enquiry_submission_via_home_page(self):
        initial_count = Enquiry.objects.count()
        payload = {
            'name': 'Michael Davies',
            'email': 'michael@example.com',
            'phone': '+1 (555) 876-5432',
            'category': 'property_management',
            'subject': 'Portfolio Management Inquiry',
            'message': 'Looking for a dedicated management partner for 3 rental apartments.'
        }
        response = self.client.post(reverse('core:home'), data=payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Enquiry.objects.count(), initial_count + 1)
        self.assertContains(response, 'Your enquiry has been received')

    def test_invalid_enquiry_submission(self):
        initial_count = Enquiry.objects.count()
        payload = {
            'name': 'J', # Too short
            'email': 'not-an-email',
            'phone': '12', # Too short
            'category': 'general',
            'subject': 'Test',
            'message': '' # Required
        }
        response = self.client.post(reverse('core:contact'), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Enquiry.objects.count(), initial_count)
        self.assertTrue(response.context['form'].errors)


class PropertyListingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.prop_sale = Property.objects.create(
            title="Modern Hillside Villa",
            slug="modern-hillside-villa",
            listing_type="sale",
            property_type="residential",
            price=650000.00,
            location="Pine Valley",
            bedrooms=4,
            bathrooms=3,
            area_sqft=3200,
            description="Spectacular contemporary home with panoramic views."
        )
        self.prop_rent = Property.objects.create(
            title="City Center Executive Suite",
            slug="city-center-executive-suite",
            listing_type="rent",
            property_type="commercial",
            price=2800.00,
            location="Metropolitan Plaza",
            description="Fully serviced commercial office floor."
        )

    def test_properties_listing_and_filtering(self):
        # All listings
        response = self.client.get(reverse('core:properties'))
        self.assertContains(response, "Modern Hillside Villa")
        self.assertContains(response, "City Center Executive Suite")

        # For Sale only
        response_sale = self.client.get(reverse('core:properties') + '?type=sale')
        self.assertContains(response_sale, "Modern Hillside Villa")
        self.assertNotContains(response_sale, "City Center Executive Suite")

        # For Rent only
        response_rent = self.client.get(reverse('core:properties') + '?type=rent')
        self.assertContains(response_rent, "City Center Executive Suite")
        self.assertNotContains(response_rent, "Modern Hillside Villa")



class DashboardSecurityAndFunctionalityTests(TestCase):
    def setUp(self):
        self.client = Client()
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.staff_user = User.objects.create_user(
            username='staff_member',
            password='Password123!',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='regular_customer',
            password='Password123!',
            is_staff=False
        )
        self.sample_enquiry = Enquiry.objects.create(
            name="David Copper",
            email="david@example.com",
            phone="+1 (555) 345-6789",
            category="construction_commercial",
            subject="Retail fit-out",
            message="Need commercial fit-out for 2000 sqft store."
        )

    def test_dashboard_unauthenticated_redirects_to_login(self):
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('core:dashboard_login'), response.url)

    def test_dashboard_regular_user_access_blocked(self):
        self.client.login(username='regular_customer', password='Password123!')
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('core:dashboard_login'), response.url)

    def test_dashboard_staff_user_successful_access(self):
        self.client.login(username='staff_member', password='Password123!')
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')
        self.assertContains(response, 'Customer Enquiries & Leads')
        self.assertContains(response, 'David Copper')

    def test_toggle_enquiry_status(self):
        self.client.login(username='staff_member', password='Password123!')
        self.assertFalse(self.sample_enquiry.is_reviewed)
        
        response = self.client.post(reverse('core:toggle_enquiry_status', args=[self.sample_enquiry.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        
        self.sample_enquiry.refresh_from_db()
        self.assertTrue(self.sample_enquiry.is_reviewed)

    def test_export_enquiries_csv(self):
        self.client.login(username='staff_member', password='Password123!')
        response = self.client.get(reverse('core:export_enquiries_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment; filename="unique_customer_enquiries.csv"', response['Content-Disposition'])
        self.assertContains(response, 'David Copper')
        self.assertContains(response, 'Commercial Construction')
