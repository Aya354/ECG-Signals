# Generated by Django 4.2.13 on 2024-06-28 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0003_customuser_alter_userprofile_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CustomUser',
            new_name='RegisterUser',
        ),
    ]
