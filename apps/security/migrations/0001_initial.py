# Generated by Django 4.1.7 on 2023-03-20 16:09

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id_card', models.CharField(db_index=True, max_length=11, verbose_name='ID card')),
                ('image', models.ImageField(blank=True, default='AvatarImage0.jpg', null=True, upload_to='users', verbose_name='Image')),
                ('gender', models.PositiveSmallIntegerField(choices=[(1, 'Male'), (2, 'Female')], default=1, verbose_name='Gender')),
                ('address', models.CharField(blank=True, max_length=150, null=True, verbose_name='Address')),
                ('landline', models.CharField(blank=True, max_length=50, null=True, verbose_name='Landline')),
                ('mobile_phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Mobile phone')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['-id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Audit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Created date')),
                ('edited_date', models.DateField(auto_now=True, verbose_name='Edited date')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Edited date')),
                ('action', models.PositiveSmallIntegerField(choices=[(1, 'Create'), (2, 'List'), (3, 'Edit'), (4, 'Delete'), (5, 'Print'), (6, 'Consult')], default=1, verbose_name='Action')),
                ('access', models.CharField(db_index=True, max_length=150, verbose_name='Access')),
                ('date_time', models.DateTimeField(auto_now_add=True, verbose_name='Date-Time')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Audit',
                'verbose_name_plural': 'Audits',
                'ordering': ['date_time'],
            },
        ),
    ]
