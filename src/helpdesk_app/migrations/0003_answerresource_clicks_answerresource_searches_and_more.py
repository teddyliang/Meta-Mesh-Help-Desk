# Generated by Django 4.1.8 on 2023-04-19 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk_app', '0002_category_answerresource_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='answerresource',
            name='clicks',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='answerresource',
            name='searches',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='answerresource',
            name='thumbsUps',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
