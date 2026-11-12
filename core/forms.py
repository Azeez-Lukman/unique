from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'phone', 'category', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-brand-charcoal focus:outline-none focus:border-brand-green focus:ring-1 focus:ring-brand-green transition text-sm',
                'placeholder': 'Your Full Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-brand-charcoal focus:outline-none focus:border-brand-green focus:ring-1 focus:ring-brand-green transition text-sm',
                'placeholder': 'name@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-brand-charcoal focus:outline-none focus:border-brand-green focus:ring-1 focus:ring-brand-green transition text-sm',
                'placeholder': '+1 (555) 000-0000',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'brand-select w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-brand-charcoal focus:outline-none focus:border-brand-green focus:ring-1 focus:ring-brand-green transition text-sm cursor-pointer',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-brand-charcoal focus:outline-none focus:border-brand-green focus:ring-1 focus:ring-brand-green transition text-sm',
                'placeholder': 'Brief summary of your project or enquiry',
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-brand-border bg-white text-brand-charcoal focus:outline-none focus:border-brand-green focus:ring-1 focus:ring-brand-green transition text-sm',
                'rows': 4,
                'placeholder': 'Tell us more about your construction project, property requirements, or questions...',
                'required': True
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Please provide your full name.")
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if len(phone) < 6:
            raise forms.ValidationError("Please provide a valid phone number.")
        return phone

