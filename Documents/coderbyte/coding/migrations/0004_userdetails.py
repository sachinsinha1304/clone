# Generated by Django 4.2.2 on 2023-06-19 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0003_test_status_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('email', models.CharField(max_length=40)),
                ('gender', models.CharField(max_length=1)),
                ('contact', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=40)),
            ],
        ),
    ]