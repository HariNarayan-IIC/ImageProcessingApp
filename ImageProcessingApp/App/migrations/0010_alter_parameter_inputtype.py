# Generated by Django 5.0.6 on 2024-06-13 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0009_alter_parameter_datatype_alter_parameter_inputtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='inputType',
            field=models.CharField(choices=[('number', 'Number'), ('text', 'String'), ('select', 'DropDown'), ('radio', 'Radio buttons'), ('checkbox', 'Checkbox'), ('range', 'Slider')], max_length=50),
        ),
    ]