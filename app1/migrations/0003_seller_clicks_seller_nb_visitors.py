# Generated by Django 4.2.3 on 2023-07-16 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='clicks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='seller',
            name='nb_visitors',
            field=models.IntegerField(default=0),
        ),
    ]
