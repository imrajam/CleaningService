# Generated by Django 3.1.7 on 2021-03-23 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0015_owner_order_table_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner_order_table',
            name='deliver',
            field=models.BooleanField(default=False),
        ),
    ]