# Generated by Django 3.1.7 on 2021-08-15 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fudaichatapp', '0003_auto_20210421_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fudaichatapp.response'),
        ),
    ]