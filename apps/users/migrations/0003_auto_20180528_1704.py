# Generated by Django 2.0.5 on 2018-05-28 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180527_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(blank=True, help_text='手机号', max_length=11, null=True, verbose_name='电话'),
        ),
    ]