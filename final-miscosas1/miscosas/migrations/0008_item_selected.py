# Generated by Django 3.0.3 on 2020-05-26 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miscosas', '0007_auto_20200526_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='selected',
            field=models.BooleanField(default=True),
        ),
    ]