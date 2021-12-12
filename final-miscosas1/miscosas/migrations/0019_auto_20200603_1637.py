# Generated by Django 3.0.3 on 2020-06-03 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miscosas', '0018_auto_20200601_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='alimentador',
            name='puntuacion',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='puntuacion',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profilephoto',
            name='foto_perfil',
            field=models.FileField(blank=True, null=True, upload_to='miscosas/media/'),
        ),
    ]
