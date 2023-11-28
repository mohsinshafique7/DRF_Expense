# Generated by Django 4.2.7 on 2023-11-25 01:07
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'category',
                    models.CharField(
                        choices=[('SALARY', 'SALARY'), ('BUSINESS', 'BUSINESS'), ('SIDE-HUSTLES', 'SIDE-HUSTLES'),
                                 ('OTHERS', 'OTHERS')],
                        max_length=25
                    )
                ),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, max_length=255)),
                ('description', models.TextField()),
                ('date', models.DateField(blank=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
