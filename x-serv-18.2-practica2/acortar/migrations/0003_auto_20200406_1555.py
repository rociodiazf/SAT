# Generated by Django 3.0.3 on 2020-04-06 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acortar', '0002_auto_20200406_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contenido',
            name='valor',
            field=models.TextField(),
        ),
    ]
