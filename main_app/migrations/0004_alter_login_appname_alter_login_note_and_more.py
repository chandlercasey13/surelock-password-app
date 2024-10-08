# Generated by Django 5.0.7 on 2024-08-02 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_login_appname_alter_login_note_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='appname',
            field=models.CharField(default='No App Name', max_length=100),
        ),
        migrations.AlterField(
            model_name='login',
            name='note',
            field=models.TextField(default='Nothing Here', max_length=250),
        ),
        migrations.AlterField(
            model_name='login',
            name='password',
            field=models.CharField(default='No Password', max_length=100),
        ),
        migrations.AlterField(
            model_name='login',
            name='username',
            field=models.CharField(default='No Username', max_length=100),
        ),
    ]
