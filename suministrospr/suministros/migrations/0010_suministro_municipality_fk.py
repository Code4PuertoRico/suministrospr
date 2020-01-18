# Generated by Django 2.2.9 on 2020-01-17 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('suministros', '0009_auto_20200117_2313'),
    ]

    operations = [
        migrations.AddField(
            model_name="suministro",
            name="municipality_fk",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="suministros",
                related_query_name="suministro",
                to="suministros.Municipality",
            ),
        ),
    ]
