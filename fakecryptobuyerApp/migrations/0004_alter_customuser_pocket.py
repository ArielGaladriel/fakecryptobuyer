# Generated by Django 4.0.5 on 2022-07-14 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fakecryptobuyerApp', '0003_alter_customuser_pocket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='pocket',
            field=models.JSONField(default=dict, verbose_name='user pocket'),
        ),
    ]
