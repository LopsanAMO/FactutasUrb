# Generated by Django 2.0.3 on 2018-04-15 23:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('facturas', '0002_auto_20180415_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]