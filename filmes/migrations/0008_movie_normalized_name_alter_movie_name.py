# Generated by Django 5.1.4 on 2025-01-08 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmes', '0007_alter_movie_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='normalized_name',
            field=models.CharField(default='', editable=False, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='name',
            field=models.CharField(error_messages={'unique': 'Filme com este nome já existe.'}, max_length=244, unique=True),
        ),
    ]
