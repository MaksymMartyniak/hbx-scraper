# Generated by Django 4.0.5 on 2022-06-04 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothing',
            name='category',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='clothing',
            name='sub_category',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='clothing',
            name='brand',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='clothing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
