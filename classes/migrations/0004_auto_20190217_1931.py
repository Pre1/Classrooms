# Generated by Django 2.1.5 on 2019-02-17 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0003_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='exam_grade',
            field=models.DecimalField(decimal_places=3, max_digits=4),
        ),
    ]
