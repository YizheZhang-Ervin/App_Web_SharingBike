# Generated by Django 3.1.5 on 2021-01-17 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bikesys', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=99.99, max_digits=8),
        ),
    ]
