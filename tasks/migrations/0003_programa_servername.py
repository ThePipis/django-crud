# Generated by Django 5.0.4 on 2024-04-29 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_programa_alter_task_datacompleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='programa',
            name='servername',
            field=models.CharField(default='', max_length=200),
        ),
    ]
