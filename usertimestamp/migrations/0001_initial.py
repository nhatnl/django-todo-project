# Generated by Django 3.2 on 2021-05-06 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserTimeStamp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.IntegerField()),
            ],
        ),
    ]