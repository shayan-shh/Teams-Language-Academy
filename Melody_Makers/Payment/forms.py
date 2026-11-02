from django import forms
from .models import Order

class PaymentForm(forms.Form):
    card_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'نام'}), required=True)
    card_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'شماره کارت'}), required=True)
    card_exp_date = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'تایخ انقضا'}), required=True)
    card_cvv_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'cvv '}), required=True)
    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={'class':'form-control','placeholder': '  name@example.com'}), required=True)
    card_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'خیابان'}), required=False)
    card_address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'خیابان دوم'}), required=False)
    card_zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'کد پستی'}), required=False)
    card_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'شهر'}),required=False)
    card_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'استان'}),required=False)
    card_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'کشور'}),required=False)

