# Generated by Django 5.0 on 2023-12-11 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget_tracker', '0004_alter_userprofile_savings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='savings',
            field=models.FloatField(),
        ),
    ]
