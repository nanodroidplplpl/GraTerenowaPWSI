# Generated by Django 4.2 on 2023-04-05 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gra', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sesje',
            name='password',
            field=models.CharField(default='', max_length=200),
        ),
    ]
