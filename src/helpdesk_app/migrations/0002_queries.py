# Generated by Django 4.1.7 on 2023-04-05 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Queries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=1000)),
                ('occurrences', models.PositiveIntegerField()),
            ],
        ),
    ]
