# Generated by Django 5.0.4 on 2024-04-29 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_programa_servername'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='programa',
            options={'ordering': ['-installdate'], 'verbose_name': 'Programa', 'verbose_name_plural': 'Programas'},
        ),
    ]