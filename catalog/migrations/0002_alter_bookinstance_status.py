# Generated by Django 3.2.9 on 2021-12-02 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('a', 'Available for adoption'), ('d', 'adopted'), ('r', 'receiving')], default='a', help_text='Adoption availability', max_length=1),
        ),
    ]
