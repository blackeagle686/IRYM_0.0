# Generated by Django 5.2 on 2025-07-03 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_logging_chat_logging_user_alter_chat_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='generated_image',
        ),
    ]
