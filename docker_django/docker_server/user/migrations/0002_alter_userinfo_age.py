# Generated by Django 4.2.6 on 2023-11-09 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='age',
            field=models.IntegerField(blank=True, default='', null=True),
        ),
    ]
