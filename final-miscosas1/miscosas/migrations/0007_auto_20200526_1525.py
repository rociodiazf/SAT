# Generated by Django 3.0.3 on 2020-05-26 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miscosas', '0006_profilephoto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilephoto',
            name='foto_perfil',
            field=models.ImageField(blank=True, null=True, upload_to='static/miscosas/profilePhoto/'),
        ),
    ]