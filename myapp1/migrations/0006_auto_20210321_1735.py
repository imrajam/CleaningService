# Generated by Django 3.1.7 on 2021-03-21 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0005_auto_20210321_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='p_discription',
            field=models.TextField(default=''),
        ),
    ]
