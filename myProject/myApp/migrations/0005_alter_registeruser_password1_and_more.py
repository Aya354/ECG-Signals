# Generated by Django 4.2.13 on 2024-06-28 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0004_rename_customuser_registeruser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeruser',
            name='password1',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='registeruser',
            name='password2',
            field=models.CharField(max_length=50),
        ),
    ]