# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-02 12:57
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import openslides.utils.models


def add_votecollector(apps, schema_editor):
    """
    Adds the one and only votecollector.
    """
    # We get the model from the versioned app registry;
    # if we directly import it, it will be the wrong version.
    model = apps.get_model('openslides_votecollector', 'VoteCollector')
    # We use bulk_create here because we do not want model's save() method
    # to be called because we do not want our autoupdate signals to be
    # triggered.
    model.objects.bulk_create([model()])


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('motions', '0002_misc_features'),
        ('assignments', '0002_assignmentpoll_pollmethod'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentPollKeypadConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('serial_number', models.CharField(max_length=255, null=True)),
                ('candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_permissions': (),
            },
            bases=(openslides.utils.models.RESTModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Keypad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keypad_id', models.IntegerField(unique=True)),
                ('battery_level', models.SmallIntegerField(default=-1)),
                ('in_range', models.BooleanField(default=False)),
            ],
            options={
                'default_permissions': (),
            },
            bases=(openslides.utils.models.RESTModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MotionPollKeypadConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('serial_number', models.CharField(max_length=255, null=True)),
                ('keypad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='openslides_votecollector.Keypad')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keypad_data_list', to='motions.MotionPoll')),
            ],
            options={
                'default_permissions': (),
            },
            bases=(openslides.utils.models.RESTModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=255)),
                ('seating_plan_x_axis', models.PositiveIntegerField()),
                ('seating_plan_y_axis', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ('pk',),
                'default_permissions': (),
            },
            bases=(openslides.utils.models.RESTModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='VoteCollector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_status', models.CharField(default='No device', max_length=200)),
                ('voting_mode', models.CharField(max_length=50, null=True)),
                ('voting_target', models.IntegerField(default=0)),
                ('voting_duration', models.IntegerField(default=0)),
                ('voters_count', models.IntegerField(default=0)),
                ('votes_received', models.IntegerField(default=0)),
                ('is_voting', models.BooleanField(default=False)),
            ],
            options={
                'permissions': (('can_manage_votecollector', 'Can manage VoteCollector'),),
                'default_permissions': (),
            },
            bases=(openslides.utils.models.RESTModelMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='seat',
            unique_together=set([('seating_plan_x_axis', 'seating_plan_y_axis')]),
        ),
        migrations.AddField(
            model_name='keypad',
            name='seat',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='openslides_votecollector.Seat'),
        ),
        migrations.AddField(
            model_name='keypad',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assignmentpollkeypadconnection',
            name='keypad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='openslides_votecollector.Keypad'),
        ),
        migrations.AddField(
            model_name='assignmentpollkeypadconnection',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keypad_data_list', to='assignments.AssignmentPoll'),
        ),
        migrations.RunPython(
            add_votecollector
        ),
    ]
