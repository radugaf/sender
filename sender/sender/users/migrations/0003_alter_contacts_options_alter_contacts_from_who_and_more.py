# Generated by Django 4.1.9 on 2023-06-14 07:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_contacts"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="contacts",
            options={"verbose_name_plural": "Contacts"},
        ),
        migrations.AlterField(
            model_name="contacts",
            name="from_who",
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name="contacts",
            name="text",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="contacts",
            name="to",
            field=models.CharField(max_length=250),
        ),
    ]
