# Generated by Django 4.0.1 on 2022-01-19 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sso', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlackListedToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='token_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('token', 'user')},
            },
        ),
    ]