# Generated by Django 4.1.8 on 2023-04-19 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk_app', '0004_alter_query_encoded_query'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='helpdesk_app.category'),
        ),
    ]