# Generated by Django 3.0.3 on 2020-06-12 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miscosas', '0024_vote_fecha'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='fecha',
        ),
    ]
