# Generated by Django 3.1.4 on 2020-12-13 22:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('medical_history', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalappointmentsummary',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='medical_appointment_summaries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='medicalappointmentimage',
            name='medical_appointment_summary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='medical_history.medicalappointmentsummary'),
        ),
    ]
