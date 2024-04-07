# Generated by Django 4.2.11 on 2024-04-07 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_expirationalerts'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='alert_activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='days_since_alert_activated',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='days_to_activate_alert',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='expirationalerts',
            name='number_of_days',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.SmallIntegerField(),
        ),
    ]