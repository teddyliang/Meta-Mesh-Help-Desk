# Generated by Django 4.1.7 on 2023-03-22 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk_app', '0005_alter_answerresource_tags'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Keyword',
        ),
    ]