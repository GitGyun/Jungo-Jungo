# Generated by Django 2.0.5 on 2018-06-06 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jungo', '0002_auto_20180605_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pstate',
            field=models.IntegerField(default=0),
        ),
    ]
