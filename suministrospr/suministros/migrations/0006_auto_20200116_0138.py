# Generated by Django 2.2.9 on 2020-01-16 01:38

import uuid

import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields
from django.db import migrations, models

import suministrospr.utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ("suministros", "0005_auto_20200115_2301"),
    ]

    operations = [
        migrations.CreateModel(
            name="Municipality",
            fields=[
                (
                    "created_at",
                    suministrospr.utils.fields.DateTimeCreatedField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "modified_at",
                    suministrospr.utils.fields.DateTimeModifiedField(
                        default=django.utils.timezone.now, editable=False
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("adjuntas", "Adjuntas"),
                            ("aguada", "Aguada"),
                            ("aguadilla", "Aguadilla"),
                            ("aguas-buenas", "Aguas Buenas"),
                            ("aibonito", "Aibonito"),
                            ("anasco", "Añasco"),
                            ("arecibo", "Arecibo"),
                            ("arroyo", "Arroyo"),
                            ("barceloneta", "Barceloneta"),
                            ("barranquitas", "Barranquitas"),
                            ("bayamon", "Bayamón"),
                            ("cabo-rojo", "Cabo Rojo"),
                            ("caguas", "Caguas"),
                            ("camuy", "Camuy"),
                            ("canovanas", "Canóvanas"),
                            ("carolina", "Carolina"),
                            ("catano", "Catano"),
                            ("cayey", "Cayey"),
                            ("ceiba", "Ceiba"),
                            ("ciales", "Ciales"),
                            ("cidra", "Cidra"),
                            ("coamo", "Coamo"),
                            ("comerio", "Comerío"),
                            ("corozal", "Corozal"),
                            ("culebra", "Culebra"),
                            ("dorado", "Dorado"),
                            ("fajardo", "Fajardo"),
                            ("florida", "Florida"),
                            ("guanica", "Guánica"),
                            ("guayama", "Guayama"),
                            ("guayanilla", "Guayanilla"),
                            ("guaynabo", "Guaynabo"),
                            ("gurabo", "Gurabo"),
                            ("hatillo", "Hatillo"),
                            ("hormigueros", "Hormigueros"),
                            ("humacao", "Humacao"),
                            ("isabela", "Isabela"),
                            ("jayuya", "Jayuya"),
                            ("juana-diaz", "Juana Díaz"),
                            ("juncos", "Juncos"),
                            ("lajas", "Lajas"),
                            ("lares", "Lares"),
                            ("las-marias", "Las Marías"),
                            ("las-piedras", "Las Piedras"),
                            ("loiza", "Loiza"),
                            ("luquillo", "Luquillo"),
                            ("manati", "Manatí"),
                            ("maricao", "Maricao"),
                            ("maunabo", "Maunabo"),
                            ("mayaguez", "Mayagüez"),
                            ("moca", "Moca"),
                            ("morovis", "Morovis"),
                            ("naguabo", "Naguabo"),
                            ("naranjito", "Naranjito"),
                            ("orocovis", "Orocovis"),
                            ("patillas", "Patillas"),
                            ("penuelas", "Peñuelas"),
                            ("ponce", "Ponce"),
                            ("quebradillas", "Quebradillas"),
                            ("rincon", "Rincón"),
                            ("rio-grande", "Río Grande"),
                            ("sabana-grande", "Sabana Grande"),
                            ("salinas", "Salinas"),
                            ("san-german", "San Germán"),
                            ("san-juan", "San Juan"),
                            ("san-lorenzo", "San Lorenzo"),
                            ("san-sebastian", "San Sebastián"),
                            ("santa-isabel", "Santa Isabel"),
                            ("toa-alta", "Toa Alta"),
                            ("toa-baja", "Toa Baja"),
                            ("trujillo-alto", "Trujillo Alto"),
                            ("utuado", "Utuado"),
                            ("vega-alta", "Vega Alta"),
                            ("vega-baja", "Vega Baja"),
                            ("vieques", "Vieques"),
                            ("villalba", "Villalba"),
                            ("yabucoa", "Yabucoa"),
                            ("yauco", "Yauco"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True,
                        editable=False,
                        max_length=255,
                        populate_from=["name"],
                    ),
                ),
            ],
            options={
                "verbose_name": "municipality",
                "verbose_name_plural": "municipalities",
            },
        ),
        migrations.AlterModelOptions(
            name="suministro",
            options={
                "verbose_name": "suministro",
                "verbose_name_plural": "suministros",
            },
        ),
        migrations.AlterField(
            model_name="suministro",
            name="municipality",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="suministros",
                related_query_name="suministro",
                to="suministros.Municipality",
            ),
        ),
    ]