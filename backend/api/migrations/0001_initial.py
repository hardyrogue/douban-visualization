# Generated by Django 5.1.7 on 2025-04-01 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('year', models.IntegerField()),
                ('director', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=100)),
                ('rating', models.FloatField()),
                ('cover', models.URLField(blank=True)),
            ],
        ),
    ]
