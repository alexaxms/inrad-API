# Generated by Django 3.1.4 on 2021-03-20 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("medical_history", "0006_auto_20210307_2244"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="patientattachmentdata",
            name="link",
        ),
        migrations.AddField(
            model_name="patientattachmentdata",
            name="attachment",
            field=models.FileField(default=None, upload_to=""),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="patientdiagnostic",
            name="disease_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="diagnostics",
                to="medical_history.diseasetype",
            ),
        ),
        migrations.AlterField(
            model_name="patientdiagnostic",
            name="patient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="diagnostics",
                to="medical_history.patient",
            ),
        ),
        migrations.AlterField(
            model_name="patienttreatment",
            name="machine",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="treatments",
                to="medical_history.treatmentmachine",
            ),
        ),
        migrations.AlterField(
            model_name="patienttreatment",
            name="mode",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="treatments",
                to="medical_history.treatmentmode",
            ),
        ),
        migrations.AlterField(
            model_name="patienttreatment",
            name="patient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="treatments",
                to="medical_history.patient",
            ),
        ),
        migrations.AlterField(
            model_name="patienttreatment",
            name="treatment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="treatments",
                to="medical_history.treatment",
            ),
        ),
    ]