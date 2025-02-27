# forms.py
from django import forms
from .apartmentmodels import *


class ApartmentLoginFormAdmin(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )

class ApartmentFlatFormAdmin(forms.ModelForm):
    class Meta:
        model = ApartmentFlat
        exclude = ['password', 'apartment_name', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['flat_size'].label = "Flat Size (sq ft)"


class ApartmentFlatLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"})
    )



class ApartmentComplaintForm(forms.ModelForm):
    class Meta:
        model = ApartmentComplaint
        fields = ['subject', 'description']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe your complaint', 'rows': 4}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})

class ApartmentComplaintReplyForm(forms.ModelForm):
    class Meta:
        model = ApartmentComplaintReply
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Reply to complaint', 'rows': 3}),
        }



class ApartmentPaymentForm(forms.ModelForm):
    class Meta:
        model = ApartmentPayment
        fields = ['flat', 'amount', 'payment_date', 'payment_mode','transaction_id', 'remarks']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'payment_mode': forms.Select(attrs={'class': 'form-control'}),
            'transaction_id' : forms.TextInput(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'flat': forms.Select(attrs={'class': 'form-control'}),
        }

class ApartmentAnnouncementForm(forms.ModelForm):
    class Meta:
        model = ApartmentAnnouncement
        fields = ['title', 'message']

class ApartmentAnnouncementReplyForm(forms.ModelForm):
    class Meta:
        model = ApartmentAnnouncementReply
        fields = ['message']

class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = ApartmentFlat
        fields = ['owner_name', 'owner_contact', 'owner_email', 'flat_size']