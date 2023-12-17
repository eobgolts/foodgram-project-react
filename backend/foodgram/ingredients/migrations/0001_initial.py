# Generated by Django 4.2.7 on 2023-12-17 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='IngredientMeasurementUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measurement_unit', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='IngredientValue',
            fields=[
                ('ingredient_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='ingredients.ingredient')),
                ('amount', models.IntegerField()),
            ],
            bases=('ingredients.ingredient',),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredients.ingredientmeasurementunit'),
        ),
    ]
