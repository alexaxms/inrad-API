# Generated by Django 3.1.4 on 2021-04-03 22:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("medical_history", "0013_auto_20210403_1455"),
    ]

    operations = [
        migrations.AlterField(
            model_name="medicalappointmentsymptom",
            name="symptom",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="appointments",
                to="medical_history.symptom",
            ),
        ),
    ]
