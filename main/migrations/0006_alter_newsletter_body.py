# Generated by Django 4.0.4 on 2022-06-08 09:04

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_newsletter_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='body',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
