# Generated by Django 5.0.6 on 2024-08-30 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_product_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('whatsapp_number', models.CharField(max_length=15)),
                ('inquiry', models.TextField()),
            ],
        ),
    ]
