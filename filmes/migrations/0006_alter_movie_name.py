# Generated by Django 5.1.4 on 2025-01-07 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmes', '0005_alter_comment_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='name',
            field=models.CharField(max_length=244, unique=True),
        ),
    ]
