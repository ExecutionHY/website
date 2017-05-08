# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='modify_date',
            new_name='modification_date',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='publish_date',
            new_name='publication_date',
        ),
    ]
