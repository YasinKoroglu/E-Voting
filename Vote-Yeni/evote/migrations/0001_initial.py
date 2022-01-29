# Generated by Django 3.2.8 on 2022-01-28 09:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import evote.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_premiumuser', models.BooleanField(default=False)),
                ('ident', models.BigIntegerField(null=True, unique=True, validators=[django.core.validators.RegexValidator(code='nomatch', message='Length has to be 11', regex='^.{11}$')])),
                ('firstname', models.CharField(max_length=30, null=True)),
                ('lastname', models.CharField(max_length=30, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegisteredUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('which_vote', models.CharField(max_length=100)),
                ('l_date', models.CharField(max_length=25, null=True)),
                ('who_voted', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('v_name', models.CharField(max_length=100)),
                ('v_code', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('v_information', models.CharField(max_length=1000)),
                ('f_date', models.DateField(auto_now_add=True, null=True)),
                ('l_date', models.DateField(null=True, validators=[evote.models.present_or_future_date])),
                ('who_voted', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Candidates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_name', models.CharField(max_length=100)),
                ('which_vote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='evote.vote')),
            ],
        ),
    ]