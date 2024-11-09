# Generated by Django 5.1 on 2024-11-04 05:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_remove_register_confirm_password_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='login',
            name='id',
        ),
        migrations.RemoveField(
            model_name='login',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='login',
            name='user',
        ),
        migrations.RemoveField(
            model_name='register',
            name='id',
        ),
        migrations.RemoveField(
            model_name='register',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='register',
            name='last_login',
        ),
        migrations.AddField(
            model_name='login',
            name='email',
            field=models.EmailField(default=1, max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='login',
            name='log_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='login',
            name='password',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='login',
            name='reg_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.register'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='register',
            name='confirm_password',
            field=models.CharField(default=2, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='register',
            name='reg_id',
            field=models.AutoField(default=2, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
