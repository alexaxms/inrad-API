# Generated by Django 3.1.4 on 2020-12-27 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medical_history', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='patient_treatment',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='medical_history.patienttreatment'),
        ),
    ]