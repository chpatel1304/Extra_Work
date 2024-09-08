from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'description', 'image1', 'image2', 'image3', 'category', 'color',  # Added color here
            'price', 'offer_price', 'quantity_s', 'quantity_m', 'quantity_l',
            'quantity_xl', 'quantity_xxl'
        ]

from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'mobile']


from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'whatsapp_number', 'inquiry']



