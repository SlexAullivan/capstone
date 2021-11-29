# Generated by Django 3.2 on 2021-11-25 02:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_delete_dash'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashBoard',
            fields=[
                ('assignment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api.assignment')),
                ('submissions', models.ManyToManyField(to='api.Submission')),
            ],
        ),
    ]
