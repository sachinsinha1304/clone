# Generated by Django 4.2.2 on 2023-06-15 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0002_test_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='test_status',
            name='time',
            field=models.IntegerField(default=180),
        ),
    ]