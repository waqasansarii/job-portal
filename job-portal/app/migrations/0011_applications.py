# Generated by Django 5.1.3 on 2024-11-21 13:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_profilejobseeker_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Applied', 'Applied'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Hired', 'Hired')], default=('Applied', 'Applied'), max_length=10)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application_job', to='app.jobs')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]