# Generated by Django 5.1.3 on 2024-11-26 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_user_totp'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('token', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
