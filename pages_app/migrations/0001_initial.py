# Generated by Django 2.2 on 2020-11-12 05:26

from django.db import migrations, models
import pages_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100, validators=[pages_app.models.nameLen])),
                ('last_name', models.CharField(max_length=100, validators=[pages_app.models.nameLen])),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255, validators=[pages_app.models.passLen])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]