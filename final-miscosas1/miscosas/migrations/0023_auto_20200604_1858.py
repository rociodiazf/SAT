# Generated by Django 3.0.3 on 2020-06-04 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miscosas', '0022_remove_comentario_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilephoto',
            name='foto_perfil',
            field=models.ImageField(blank=True, null=True, upload_to='miscosas/media/'),
        ),
    ]