# Generated by Django 4.2.7 on 2024-03-12 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0008_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='model',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, to='goods.model', verbose_name='Тип'),
        ),
    ]