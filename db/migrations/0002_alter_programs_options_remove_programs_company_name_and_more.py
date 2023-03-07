# Generated by Django 4.1.7 on 2023-03-02 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="programs",
            options={},
        ),
        migrations.RemoveField(
            model_name="programs",
            name="company_name",
        ),
        migrations.RemoveField(
            model_name="programs",
            name="platform",
        ),
        migrations.RemoveField(
            model_name="programs",
            name="program_name",
        ),
        migrations.RemoveField(
            model_name="programs",
            name="program_url",
        ),
        migrations.AddField(
            model_name="programs",
            name="data",
            field=models.JSONField(null=True),
        ),
        migrations.DeleteModel(
            name="Inscope",
        ),
    ]
