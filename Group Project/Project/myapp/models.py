from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomerManager(BaseUserManager):
    def create_user(self, first_name, last_name, mobile, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not mobile:
            raise ValueError('Users must have a mobile number')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, mobile, email, password=None):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Customer(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    otp = models.CharField(max_length=4, null=True, blank=True)

    objects = CustomerManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    def __str__(self):
        return self.mobile

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

from django.db import models
import random
import string

def generate_product_code():
    letters = string.ascii_uppercase
    numbers = string.digits
    return ''.join(random.choices(letters, k=2)) + ''.join(random.choices(numbers, k=4))

class Product(models.Model):
    product_code = models.CharField(max_length=6, default=generate_product_code, unique=True)
    description = models.TextField()
    image1 = models.ImageField(upload_to='products/')
    image2 = models.ImageField(upload_to='products/')
    image3 = models.ImageField(upload_to='products/')
    
    CATEGORY_CHOICES = [
        ('Salwar-Suit', 'Salwar Suit'),
        ('Lehnga-Choli', 'Lehnga Choli'),
        ('Gown', 'Gown'),
        ('Designer-Suit', 'Designer Suit'),
        ('Jeans-Tops', 'Jeans Tops'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    color = models.CharField(max_length=30,default="No Color")  # New color field
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    quantity_s = models.PositiveIntegerField(default=0)
    quantity_m = models.PositiveIntegerField(default=0)
    quantity_l = models.PositiveIntegerField(default=0)
    quantity_xl = models.PositiveIntegerField(default=0)
    quantity_xxl = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.product_code

from django.db import models

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    whatsapp_number = models.CharField(max_length=15)
    inquiry = models.TextField()

    def __str__(self):
        return f"Appointment with {self.name}"


from django.db import models

class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
