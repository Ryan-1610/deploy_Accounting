# Generated by Django 5.0.7 on 2024-10-13 03:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='EventID',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='StudID',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]
