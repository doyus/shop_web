# Generated by Django 2.1 on 2018-09-21 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Jindong', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yonghu',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='yonghu',
            name='password',
            field=models.CharField(max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='yonghu',
            name='passwordd',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='yonghu',
            name='phone',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='yonghu',
            name='sex',
            field=models.CharField(max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='yonghu',
            name='shouhuo',
            field=models.CharField(max_length=80, unique=True),
        ),
        migrations.AlterField(
            model_name='yonghu',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]