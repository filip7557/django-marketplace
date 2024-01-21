# Generated by Django 4.2 on 2024-01-21 21:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0004_dispute_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='isActive',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ad',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dispute',
            name='isSolved',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seller',
            name='isSeller',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
