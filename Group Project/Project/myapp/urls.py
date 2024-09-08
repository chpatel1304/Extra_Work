from django.urls import path
from . import views
from .views import signup_view,change_password_view,add_product_view,view_products,get_user_profile,submit_inquiry,get_appointments,fetch_inquiries
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('change-password/', change_password_view, name='change_password'),
    path('add-products/', add_product_view, name='add-products'),
    path('view-products/', view_products, name='view-products'),
    path('view-products/<int:product_id>/', view_products, name='view-products'),
    path('profile/<str:mobile>/', get_user_profile, name='get_user_profile'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('submit-inquiry/', submit_inquiry, name='submit_inquiry'),
    path('get-appointments/', get_appointments, name='get_appointments'),
    path('inquiry-forms/',fetch_inquiries,name='inquiry-forms'),
    path('get-salwar-suits/', views.get_salwar_suits, name='get_salwar_suits'),
    path('filter-products-by-color/<str:color>/', views.filter_products_by_color, name='filter_products_by_color'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
