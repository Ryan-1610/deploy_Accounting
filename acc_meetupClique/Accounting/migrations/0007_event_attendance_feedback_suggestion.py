# Generated by Django 5.0.7 on 2024-10-13 04:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting', '0006_remove_event_staffid_remove_feedback_studid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('EventID', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('EventName', models.CharField(max_length=30)),
                ('EventDetails', models.CharField(max_length=100)),
                ('EventDate', models.DateField()),
                ('EventTime', models.TimeField()),
                ('EventStatus', models.CharField(max_length=10)),
                ('StaffID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounting.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('AttendanceID', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('AttStatus', models.CharField(max_length=10)),
                ('StudID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounting.student')),
                ('EventID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounting.event')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('FeedbackID', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('EventRating', models.IntegerField()),
                ('Comment', models.CharField(max_length=100)),
                ('EventID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounting.event')),
                ('StudID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounting.student')),
            ],
        ),
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('SuggestionID', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('Suggestion', models.CharField(max_length=100)),
                ('StudID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounting.student')),
            ],
        ),
    ]
