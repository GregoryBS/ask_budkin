# Generated by Django 2.2 on 2020-11-14 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='rating',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(db_index=True, max_length=30, unique=True, verbose_name='Title of tag'),
        ),
    ]
