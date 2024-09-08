from django.contrib import admin
from .models import Customer, Product,Appointment,Inquiry

# Register the Customer model using the @admin.register decorator
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'mobile', 'email', 'is_active', 'is_admin')
    search_fields = ('first_name', 'last_name', 'mobile', 'email')
    list_filter = ('is_active', 'is_admin')
    ordering = ('first_name',)

# Register the Product model using the admin.site.register function
admin.site.register(Product)
admin.site.register(Inquiry)
from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'whatsapp_number', 'inquiry')

