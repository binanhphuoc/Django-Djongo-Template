# Generated by Django 2.2.7 on 2019-11-14 03:32

from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('solver', '0005_auto_20191114_0325'),
    ]

    operations = [
        migrations.AddField(
            model_name='concept',
            name='attributes',
            field=djongo.models.fields.ArrayReferenceField(blank=True, default=list, on_delete=djongo.models.fields.ArrayReferenceField._on_delete, to='solver.Attribute'),
        ),
        migrations.AddField(
            model_name='concept',
            name='equations',
            field=djongo.models.fields.ArrayReferenceField(blank=True, default=list, on_delete=djongo.models.fields.ArrayReferenceField._on_delete, to='solver.Equation'),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='parent_concept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solver.Concept'),
        ),
        migrations.AlterField(
            model_name='equation',
            name='parent_concept',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solver.Concept'),
        ),
    ]
