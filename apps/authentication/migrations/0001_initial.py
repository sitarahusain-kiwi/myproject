# Generated by Django 3.2.10 on 2022-09-26 06:22

import apps.authentication.managers
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='last name')),
                ('username', models.CharField(blank=True, max_length=50, verbose_name='username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('email_verification_token', models.CharField(blank=True, max_length=256, verbose_name='email verification token')),
                ('email_verification_otp', models.CharField(blank=True, max_length=256, verbose_name='email verification token')),
                ('password_otp', models.CharField(blank=True, max_length=256, verbose_name='password token')),
                ('password_hashcode', models.CharField(blank=True, max_length=256, verbose_name='password hashcode')),
                ('email_verified', models.BooleanField(default=False, verbose_name='email verification status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'auth_users',
            },
            managers=[
                ('objects', apps.authentication.managers.UserManager()),
            ],
        ),
    ]
