# Generated by Django 4.2.7 on 2024-03-12 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0009_product_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloth',
            name='images',
            field=models.ImageField(blank=True, upload_to='products/clothes/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ImageField(upload_to='products/shoes/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='model',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, to='goods.model', verbose_name='Модель'),
        ),
        migrations.CreateModel(
            name='Accessory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Цена')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('on_sale', models.BooleanField(default=False)),
                ('images', models.ImageField(upload_to='products/accessory/')),
                ('brand', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='goods.brand', verbose_name='Бренд')),
                ('model', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, to='goods.model', verbose_name='Модель')),
                ('type', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='goods.type', verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Аксессуар',
                'verbose_name_plural': 'Аксессуары',
            },
        ),
    ]
