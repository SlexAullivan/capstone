# Generated by Django 3.2 on 2021-10-12 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='pointsPossible',
            field=models.FloatField(default=0),
        ),
    ]
