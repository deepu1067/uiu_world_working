# Generated by Django 4.2.1 on 2023-08-06 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metamesh', '0008_rename__id_posts_iid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='upvote',
            field=models.CharField(default='0', max_length=100, null=True),
        ),
    ]
