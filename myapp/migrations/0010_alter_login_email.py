# Generated by Django 5.1 on 2024-11-06 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_register_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]