# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 22:17
from __future__ import unicode_literals

from django.db import migrations, models
import proposal.models


class Migration(migrations.Migration):

    dependencies = [
        ('proposal', '0005_auto_20161204_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='other_addresses',
            field=models.CharField(help_text='Other addresses covered by this proposal', max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(null=True, upload_to=proposal.models.upload_document_to),
        ),
        migrations.AlterField(
            model_name='document',
            name='thumbnail',
            field=models.FileField(null=True, upload_to=proposal.models.upload_document_to),
        ),
        migrations.AlterField(
            model_name='event',
            name='proposals',
            field=models.ManyToManyField(related_name='events', related_query_name='event', to='proposal.Proposal'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.FileField(null=True, upload_to=proposal.models.upload_image_to),
        ),
    ]