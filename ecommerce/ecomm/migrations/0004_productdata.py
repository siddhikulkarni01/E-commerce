# Generated by Django 5.0.4 on 2024-04-06 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomm', '0003_userdata_delete_userdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='Productdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/')),
                ('price', models.IntegerField()),
            ],
        ),
    ]