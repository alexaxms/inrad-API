# Generated by Django 3.1.4 on 2021-02-15 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medical_history', '0003_auto_20210215_0148'),
    ]

    operations = [
        migrations.CreateModel(
            name='TreatmentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='treatment',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='treatments', to='medical_history.treatmentcategory'),
            preserve_default=False,
        ),
    ]
