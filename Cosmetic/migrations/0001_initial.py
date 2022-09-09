# Generated by Django 4.1.1 on 2022-09-09 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_address', models.BooleanField(blank=True, null=True, verbose_name='work address')),
                ('address1', models.CharField(max_length=255, verbose_name='address1')),
                ('address2', models.CharField(blank=True, max_length=255, null=True, verbose_name='address2')),
                ('phone', models.CharField(max_length=255, verbose_name='phone')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Brand_Name', models.CharField(max_length=200, verbose_name='Brand_Name')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('is_active', models.BooleanField(verbose_name='is active')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='Cosmetic.category', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='city')),
            ],
            options={
                'verbose_name': 'city',
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_qty', models.IntegerField(verbose_name='item_qty')),
                ('ordered', models.BooleanField(default=False, verbose_name='ordered')),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('NEW', 'New'), ('PROCESSING', 'New'), ('SHIPPED', 'Shipped'), ('COMPLETED', 'Completed'), ('REFUNDED', 'Refunded')], max_length=255, verbose_name='title')),
                ('is_default', models.BooleanField(verbose_name='is default')),
            ],
            options={
                'verbose_name': 'OrderStatus',
                'verbose_name_plural': 'order statuses',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Product_Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('ingredient', models.TextField(blank=True, null=True, verbose_name='ingredient')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
                ('discounted_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='discounted price')),
                ('is_active', models.BooleanField(verbose_name='is active')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Cosmetic.brand')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='Cosmetic.category', verbose_name='category')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(blank=True, decimal_places=0, max_digits=1000, null=True, verbose_name='total')),
                ('ordered', models.BooleanField(verbose_name='ordered')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Cosmetic.address', verbose_name='address')),
                ('items', models.ManyToManyField(related_name='order', to='Cosmetic.item', verbose_name='items')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='Cosmetic.orderstatus', verbose_name='status')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cosmetic.product', verbose_name='product'),
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=50, verbose_name='Product_Color')),
                ('imageUrl', models.URLField(max_length=255)),
                ('productName', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Cosmetic.product', verbose_name='Product_Name')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='Cosmetic.city'),
        ),
    ]
