# Generated by Django 4.1.6 on 2023-02-03 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hazeapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='size',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]
