# Generated by Django 5.0.6 on 2024-06-07 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_category_operations_parameters'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Attributes',
            new_name='Attribute',
        ),
        migrations.RenameModel(
            old_name='Operations',
            new_name='Operation',
        ),
        migrations.RenameModel(
            old_name='Parameters',
            new_name='Parameter',
        ),
    ]