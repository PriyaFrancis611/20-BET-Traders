# Generated by Django 5.1.3 on 2024-12-16 19:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_payment_history2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promo_code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promo_code_id', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user8', to='app.profile')),
            ],
        ),
    ]