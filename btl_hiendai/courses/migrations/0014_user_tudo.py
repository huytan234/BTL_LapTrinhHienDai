# Generated by Django 4.2.13 on 2024-05-29 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_remove_surveyresponse_user_surveyform_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tuDo',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='courses.tudo'),
        ),
    ]
