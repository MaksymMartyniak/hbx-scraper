# Generated by Django 4.0.5 on 2022-06-06 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0008_alter_category_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothing',
            name='price',
            field=models.CharField(max_length=50),
        ),
    ]
