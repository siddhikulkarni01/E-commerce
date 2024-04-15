# Generated by Django 5.0.4 on 2024-04-08 11:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0006_alter_order_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm.productdata')),
            ],
        ),
    ]