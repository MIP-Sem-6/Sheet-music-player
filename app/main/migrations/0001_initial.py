# Generated by Django 3.0.8 on 2021-02-04 02:56

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
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('album', models.CharField(blank=True, max_length=100)),
                ('tags', models.CharField(blank=True, max_length=50)),
                ('cover_image', models.ImageField(default='default_cover.jpg', upload_to='cover_images')),
                ('play_count', models.IntegerField(default=0)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'title', 'added_date')},
            },
        ),
    ]