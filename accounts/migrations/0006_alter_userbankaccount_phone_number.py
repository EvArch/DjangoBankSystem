# Generated by Django 3.2.9 on 2022-02-21 18:45

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20220221_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbankaccount',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]