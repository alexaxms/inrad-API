# Generated by Django 3.1.4 on 2021-02-15 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medical_history', '0002_auto_20210215_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='symptom',
            name='diagnostic',
        ),
    ]