# Generated by Django 3.2.7 on 2021-11-28 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_relationship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationship',
            name='status',
            field=models.CharField(choices=[('sent', 'sent')], max_length=10),
        ),
    ]
