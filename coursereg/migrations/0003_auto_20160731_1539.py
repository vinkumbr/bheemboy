# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-31 15:39
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('coursereg', '0002_user_telephone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('points', models.DecimalField(decimal_places=3, default=Decimal('0.00'), max_digits=10)),
                ('should_count_towards_cgpa', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='term',
            name='default_last_adviser_approval_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Note: Year field is ignored', verbose_name='Deafult last adviser approval date'),
        ),
        migrations.AddField(
            model_name='term',
            name='default_last_conversion_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Note: Year field is ignored', verbose_name='Deafult last credit/audit conversion date'),
        ),
        migrations.AddField(
            model_name='term',
            name='default_last_drop_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Note: Year field is ignored', verbose_name='Deafult last drop date'),
        ),
        migrations.AddField(
            model_name='term',
            name='default_last_drop_with_mention_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Note: Year field is ignored', verbose_name='Deafult last drop with mention date'),
        ),
        migrations.AddField(
            model_name='term',
            name='default_last_grade_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Note: Year field is ignored', verbose_name='Deafult last grade date'),
        ),
        migrations.AddField(
            model_name='term',
            name='default_last_instructor_approval_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Note: Year field is ignored', verbose_name='Deafult last instructor approval date'),
        ),
        migrations.AddField(
            model_name='term',
            name='default_last_reg_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Note: Year field is ignored', verbose_name='Deafult last registration date'),
        ),
        migrations.AddField(
            model_name='course',
            name='auto_instructor_approve',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='course',
            name='auto_adviser_approve',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='course',
            name='credit_label',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Credit split (ex: 3:0)'),
        ),
        migrations.AddField(
            model_name='course',
            name='last_adviser_approval_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last adviser approval date'),
        ),
        migrations.AddField(
            model_name='course',
            name='last_instructor_approval_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last instructor approval date'),
        ),
        migrations.AddField(
            model_name='course',
            name='last_conversion_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last credit/audit conversion date'),
        ),
        migrations.AddField(
            model_name='course',
            name='last_drop_with_mention_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last drop with mention date'),
        ),
        migrations.AddField(
            model_name='course',
            name='last_grade_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last grade date'),
        ),
        migrations.AddField(
            model_name='course',
            name='num_credits',
            field=models.IntegerField(default=3, verbose_name='Number of credits'),
        ),
        migrations.AddField(
            model_name='course',
            name='should_count_towards_cgpa',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='course',
            name='year',
            field=models.CharField(default='', max_length=4),
        ),
        migrations.AddField(
            model_name='department',
            name='abbreviation',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='is_credit',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='is_drop',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='participant',
            name='is_drop_mentioned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='participant',
            name='should_count_towards_cgpa',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='last_drop_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last drop date'),
        ),
        migrations.AlterField(
            model_name='course',
            name='last_reg_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last registration date'),
        ),
        migrations.AddField(
            model_name='participant',
            name='new_grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coursereg.Grade'),
        ),
        migrations.AddField(
            model_name='course',
            name='new_term',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coursereg.Term'),
        ),

        migrations.AddField(
            model_name='degree',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='department',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='grade',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='term',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='auto_advisee_approve',
            field=models.BooleanField(default=False),
        ),
    ]
