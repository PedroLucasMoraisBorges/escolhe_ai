# Generated by Django 5.1.4 on 2025-01-08 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmes', '0008_movie_normalized_name_alter_movie_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='normalized_name',
            field=models.CharField(default='', max_length=255, null=True),
        ),
    ]
