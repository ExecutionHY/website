# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20170508_1439'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='title',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='title',
            new_name='tag',
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(verbose_name=b'category', to='blog.Category'),
        ),
    ]
