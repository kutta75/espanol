# Generated by Django 3.1.7 on 2021-03-23 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('verbos', '0003_auto_20210310_0940'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=5)),
            ],
        ),
        migrations.AlterField(
            model_name='conjugacion',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conjugacion', to='verbos.level'),
        ),
    ]
