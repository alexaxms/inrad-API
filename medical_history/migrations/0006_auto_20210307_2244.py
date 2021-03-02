# Generated by Django 3.1.4 on 2021-03-07 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medical_history', '0005_treatmentmachine_treatmentmode'),
    ]

    operations = [
        migrations.AddField(
            model_name='patienttreatment',
            name='machine',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='medical_history.treatmentmachine'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patienttreatment',
            name='mode',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='medical_history.treatmentmode'),
            preserve_default=False,
        ),
    ]
