# Generated by Django 5.1 on 2024-08-09 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StoreValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('key', models.CharField(max_length=255, unique=True)),
                ('value', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
