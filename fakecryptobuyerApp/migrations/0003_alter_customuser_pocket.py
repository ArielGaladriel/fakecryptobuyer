# Generated by Django 4.0.5 on 2022-07-14 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fakecryptobuyerApp', '0002_alter_customuser_pocket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='pocket',
            field=models.JSONField(blank=True, null=True, verbose_name='user pocket'),
        ),
    ]
