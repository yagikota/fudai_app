# Generated by Django 3.1.7 on 2021-04-18 08:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fudaichatapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='post_date',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='question',
            name='content',
        ),
        migrations.RemoveField(
            model_name='question',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='question',
            name='likes',
        ),
        migrations.AddField(
            model_name='question',
            name='body',
            field=models.TextField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fudaichatapp.response')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='fudaichatapp.question')),
            ],
        ),
    ]