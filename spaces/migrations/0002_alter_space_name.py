# Generated by Django 4.1.2 on 2023-03-28 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
