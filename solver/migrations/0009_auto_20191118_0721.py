# Generated by Django 2.2.7 on 2019-11-18 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solver', '0008_auto_20191116_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concept',
            name='name',
            field=models.TextField(blank=True, default=''),
        ),
    ]
