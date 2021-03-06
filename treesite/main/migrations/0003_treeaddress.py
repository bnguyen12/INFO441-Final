# Generated by Django 2.2.1 on 2019-05-14 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_delete_treeaddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='TreeAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=32)),
                ('zip', models.IntegerField()),
                ('trees_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Trees')),
            ],
        ),
    ]
