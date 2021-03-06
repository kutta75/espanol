# Generated by Django 3.1.7 on 2021-04-27 15:16

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('verbos', '0005_auto_20210425_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='Palabrafecha',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palabrafecha', models.DateField(default=datetime.date.today, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='palabra',
            name='fecha',
        ),
        migrations.AddField(
            model_name='palabra',
            name='palabrafecha',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='palabra', to='verbos.palabrafecha'),
        ),
    ]
