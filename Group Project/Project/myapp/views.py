from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer

@api_view(['POST'])
def signup_view(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth import authenticate
from django.http import JsonResponse
from .models import Customer
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mobile = data.get('mobile')
        password = data.get('password')

        try:
            # Check if the mobile number exists in the database
            user = Customer.objects.get(mobile=mobile)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        # Authenticate user by checking if the password is correct
        if user.check_password(password):
            # Return user details after successful authentication
            user_data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'mobile': user.mobile,
                'email': user.email,
            }
            return JsonResponse({'success': True, 'user': user_data})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
# backend/myapp/views.py

from django.core.mail import send_mail, BadHeaderError
from django.http import JsonResponse
from .models import Customer
from django.views.decorators.csrf import csrf_exempt
import json
import random
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        try:
            user = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Email not found'}, status=404)

        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.save()

        try:
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                'chpatel1304@gmail.com',
                [email],
                fail_silently=False,
            )
            return JsonResponse({'success': True})
        except BadHeaderError:
            return JsonResponse({'error': 'Invalid header found.'}, status=400)
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return JsonResponse({'error': 'Failed to send OTP. Please try again later.'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        otp = data.get('otp')
        new_password = data.get('new_password')

        try:
            user = Customer.objects.get(otp=otp)
            user.set_password(new_password)
            user.otp = None  # Clear the OTP after successful verification
            user.save()
            return JsonResponse({'success': True})
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Invalid OTP'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
# myapp/views.py
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from .models import Customer
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def change_password_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        try:
            # Fetch the user based on the email
            user = Customer.objects.get(email=email)

            # Check if the old password matches
            if not check_password(old_password, user.password):
                return JsonResponse({'error': 'Old password is incorrect'}, status=400)

            # Update the user's password
            user.password = make_password(new_password)
            user.save()

            return JsonResponse({'success': True})
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

from django.shortcuts import render
from django.http import JsonResponse
from .models import Product
from .forms import ProductForm
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def add_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Product added successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from .forms import ProductForm
import json

@csrf_exempt
def view_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        product_list = []
        for product in products:
            product_data = {
                'id': product.id,
                'product_code': product.product_code,
                'description': product.description,
                'category': product.category,
                'price': product.price,
                'offer_price': product.offer_price,
                'color': product.color,
                'quantity_s': product.quantity_s,
                'quantity_m': product.quantity_m,
                'quantity_l': product.quantity_l,
                'quantity_xl': product.quantity_xl,
                'quantity_xxl': product.quantity_xxl,
                'image1': product.image1.url if product.image1 else '',
                'image2': product.image2.url if product.image2 else '',
                'image3': product.image3.url if product.image3 else '',
            }
            product_list.append(product_data)
        return JsonResponse({'products': product_list})

    elif request.method == 'POST':
        try:
            # Extract the request body and form data separately
            if request.headers.get('Content-Type') == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            # Fetch the product based on the ID
            product = get_object_or_404(Product, id=data.get('id'))

            # Handle delete request
            if data.get('delete') == True:
                product.delete()
                return JsonResponse({'success': True, 'message': 'Product deleted successfully'})

            # Handle update request
            else:
                form = ProductForm(request.POST, request.FILES, instance=product)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'success': True, 'message': 'Product updated successfully'})
                else:
                    return JsonResponse({'success': False, 'errors': form.errors})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Customer  # Assuming 'Customer' is your user model
import json

@csrf_exempt
def get_user_profile(request, mobile):
    if request.method == 'GET':
        user = get_object_or_404(Customer, mobile=mobile)
        user_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'mobile': user.mobile
        }
        return JsonResponse(user_data)
    
    elif request.method == 'PUT':
        user = get_object_or_404(Customer, mobile=mobile)
        data = json.loads(request.body)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.save()
        return JsonResponse({'message': 'Profile updated successfully'})



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Appointment
@csrf_exempt
def book_appointment(request):
    print("Successfully 1")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            whatsapp_number = data.get('whatsapp_number')
            inquiry = data.get('inquiry')
            
            print(f"Name: {name}, WhatsApp Number: {whatsapp_number}, Inquiry: {inquiry}")
            
            # Handle the case where some fields might be empty
            errors = {}
            if not name:
                errors['name'] = 'This field is required.'
            if not whatsapp_number:
                errors['whatsapp_number'] = 'This field is required.'
            if not inquiry:
                errors['inquiry'] = 'This field is required.'

            if errors:
                print(errors)
                return JsonResponse({'success': False, 'errors': errors})
            
            # Save the data to the database
            appointment = Appointment(name=name, whatsapp_number=whatsapp_number, inquiry=inquiry)
            appointment.save()

            print("Successfully 3")
            return JsonResponse({'success': True, 'message': 'Appointment booked successfully!'})
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Inquiry
import json

@csrf_exempt
def submit_inquiry(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            number = data.get('number')
            email = data.get('email')
            message = data.get('message')

            # Validation
            if not name or not number or not email or not message:
                return JsonResponse({'success': False, 'message': 'All fields are required.'}, status=400)

            # Save the inquiry
            Inquiry.objects.create(name=name, number=number, email=email, message=message)
            
            return JsonResponse({'success': True, 'message': 'Inquiry submitted successfully!'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data.'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Appointment

@csrf_exempt
def get_appointments(request):
    if request.method == 'GET':
        appointments = Appointment.objects.all().values()
        appointments_list = list(appointments)  # Convert QuerySet to a list of dictionaries
        return JsonResponse({'success': True, 'appointments': appointments_list})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


from django.http import JsonResponse
from .models import Inquiry
@csrf_exempt
def fetch_inquiries(request):
    if request.method == 'GET':
        inquiries = Inquiry.objects.all().values()
        return JsonResponse(list(inquiries), safe=False)


from django.http import JsonResponse
from .models import Product

# Fetch all salwar suit products
@csrf_exempt
def get_salwar_suits(request):
    products = Product.objects.filter(category='Salwar-Suit')
    product_list = [{
        'id': product.id,
        'description': product.description,
        'price': product.price,
        'offer_price': product.offer_price,
        'colors': product.color,
        'images': [product.image1.url, product.image2.url, product.image3.url]
    } for product in products]
    return JsonResponse(product_list, safe=False)

# Fetch products by color
@csrf_exempt
def filter_products_by_color(request, color):
    products = Product.objects.filter(category='Salwar-Suit', color=color)
    product_list = [{
        'id': product.id,
        'description': product.description,
        'price': product.price,
        'offer_price': product.offer_price,
        'colors': product.color,
        'images': [product.image1.url, product.image2.url, product.image3.url]
    } for product in products]
    return JsonResponse(product_list, safe=False)
