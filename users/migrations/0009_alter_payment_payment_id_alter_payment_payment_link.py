# Generated by Django 4.2.7 on 2024-03-02 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_payment_payment_id_payment_payment_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.TextField(blank=True, null=True, verbose_name='номер сессии платежа'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_link',
            field=models.TextField(blank=True, null=True, verbose_name='ссылка платежа'),
        ),
    ]