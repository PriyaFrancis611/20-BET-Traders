# Generated by Django 5.1.3 on 2024-11-27 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_full_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(default='', max_length=30)),
                ('date', models.DateField()),
                ('payout', models.IntegerField()),
                ('revenue', models.IntegerField()),
                ('balance', models.IntegerField()),
                ('status', models.CharField(default='', max_length=30)),
            ],
        ),
    ]