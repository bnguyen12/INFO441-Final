# Generated by Django 2.2.1 on 2019-05-14 20:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_auto_20190514_0642'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTrees',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trees_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Trees')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
