# Generated by Django 4.2.2 on 2023-06-19 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coding', '0005_userdetails_psw'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='address',
            field=models.TextField(),
        ),
    ]
