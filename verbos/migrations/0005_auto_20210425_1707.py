# Generated by Django 3.1.7 on 2021-04-25 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('verbos', '0004_auto_20210323_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='Palabrafamilia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palabrafamilia', models.CharField(max_length=30, null=True)),
                ('palabrafamiliaseq', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Palabragenero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palabragenero', models.CharField(max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Palabranivel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palabranivel', models.CharField(max_length=2, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Palabratipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palabratipo', models.CharField(max_length=32, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='pronombre',
            name='pronombreseq',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='tiempo',
            name='tiemposeq',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='verbotipo',
            name='verbotiposeq',
            field=models.IntegerField(null=True),
        ),
        migrations.CreateModel(
            name='Palabra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('palabra', models.CharField(max_length=40, null=True)),
                ('traduccion', models.CharField(max_length=60, null=True)),
                ('palabrafamilia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='palabra', to='verbos.palabrafamilia')),
                ('palabragenero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='palabra', to='verbos.palabragenero')),
                ('palabranivel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='palabra', to='verbos.palabranivel')),
                ('palabratipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='palabra', to='verbos.palabratipo')),
            ],
        ),
    ]