# Generated by Django 2.2.9 on 2020-01-17 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('suministros', '0012_remove_suministro_municipality'),
    ]

    operations = [
        migrations.RenameField(
            model_name='suministro',
            old_name='municipality_fk',
            new_name='municipality',
        ),
    ]
