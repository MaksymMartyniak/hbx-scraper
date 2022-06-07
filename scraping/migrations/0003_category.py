# Generated by Django 4.0.5 on 2022-06-04 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_clothing_category_clothing_sub_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('gender', models.CharField(choices=[('M', 'Men'), ('W', 'Women')], default='M', max_length=3)),
                ('url', models.URLField()),
            ],
        ),
    ]
