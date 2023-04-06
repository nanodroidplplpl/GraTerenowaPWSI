# Generated by Django 4.2 on 2023-04-04 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sesje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ses_number', models.CharField(max_length=200)),
                ('end_time', models.DateTimeField(verbose_name='end date')),
            ],
        ),
        migrations.CreateModel(
            name='Gracze',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('g_nick', models.CharField(max_length=200)),
                ('score', models.IntegerField()),
                ('ses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gra.sesje')),
            ],
        ),
    ]