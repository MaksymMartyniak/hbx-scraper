# Generated by Django 4.0.5 on 2022-06-06 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0007_category_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='url',
            field=models.URLField(),
        ),
    ]
