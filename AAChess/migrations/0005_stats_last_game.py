# Generated by Django 5.0.4 on 2024-04-24 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AAChess', '0004_authtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='stats',
            name='last_game',
            field=models.CharField(default='null', max_length=10),
        ),
    ]