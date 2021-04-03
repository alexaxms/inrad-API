# Generated by Django 3.1.4 on 2021-03-28 16:34

from django.db import migrations


def initial_machines_mode(apps, schema_editor):
    from medical_history.models import TreatmentMode, TreatmentMachine

    TreatmentMode.objects.create(name="Curativa")
    TreatmentMode.objects.create(name="Paliativa")
    TreatmentMode.objects.create(name="Preoperatoria")
    TreatmentMode.objects.create(name="Sintomática")
    TreatmentMode.objects.create(name="Antiinflamatoria")

    TreatmentMachine.objects.create(name="Acelerador lineal")
    TreatmentMachine.objects.create(name="Braquiterapia HDR")
    TreatmentMachine.objects.create(name="Braquiterapia LDR")
    TreatmentMachine.objects.create(name="Implante de semillas")
    TreatmentMachine.objects.create(name="Fotodinamia")


class Migration(migrations.Migration):

    dependencies = [
        ("medical_history", "0011_auto_20210328_0519"),
    ]

    operations = [
        migrations.RunPython(initial_machines_mode),
    ]