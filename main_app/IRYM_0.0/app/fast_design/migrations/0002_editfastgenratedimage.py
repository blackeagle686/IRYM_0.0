# Generated by Django 5.2 on 2025-07-26 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fast_design', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditFastGenratedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='generated/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
