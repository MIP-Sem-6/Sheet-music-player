# Generated by Django 3.0.8 on 2021-02-04 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='file',
            field=models.FileField(default='aot.mp3', upload_to='songs'),
        ),
    ]