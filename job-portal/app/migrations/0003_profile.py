# Generated by Django 5.1.3 on 2024-11-16 10:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_project_created_by_remove_project_members_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.TextField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default=0, max_length=50)),
                ('dob', models.DateField(blank=True, null=True)),
                ('company_name', models.CharField(max_length=200)),
                ('company_size', models.IntegerField()),
                ('country', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('logo', models.FileField(blank=True, null=True, upload_to='profiles/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
