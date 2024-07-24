# Generated by Django 4.2.3 on 2024-07-24 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_input', models.TextField()),
                ('news_summary', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('news_list', models.JSONField(blank=True, default=dict, null=True)),
                ('encyc_list', models.JSONField(blank=True, default=dict, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
