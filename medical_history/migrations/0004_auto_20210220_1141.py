# Generated by Django 3.1.4 on 2021-02-20 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medical_history', '0003_remove_symptom_diagnostic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disease',
            name='stage',
        ),
        migrations.RemoveField(
            model_name='disease',
            name='type',
        ),
        migrations.RemoveField(
            model_name='treatmentsession',
            name='disease',
        ),
        migrations.RemoveField(
            model_name='treatmentsession',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='treatmentsession',
            name='patient_treatment',
        ),
        migrations.RemoveField(
            model_name='treatmentsession',
            name='user',
        ),
        migrations.RemoveField(
            model_name='treatmentsessionimage',
            name='treatment_session',
        ),
        migrations.RemoveField(
            model_name='patientdiagnostic',
            name='diagnostic',
        ),
        migrations.AddField(
            model_name='diseasetype',
            name='code',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='diseasetype',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='patientdiagnostic',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='patientdiagnostic',
            name='disease_aggressiveness',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patientdiagnostic',
            name='disease_stage',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patientdiagnostic',
            name='disease_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='medical_history.diseasetype'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Diagnostic',
        ),
        migrations.DeleteModel(
            name='Disease',
        ),
        migrations.DeleteModel(
            name='DiseaseStage',
        ),
        migrations.DeleteModel(
            name='TreatmentSession',
        ),
        migrations.DeleteModel(
            name='TreatmentSessionImage',
        ),
    ]