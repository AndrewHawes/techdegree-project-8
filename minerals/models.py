from django.db import models
from django.db.models import CharField, TextField


class DisplayField:
    """
    Generates individual field with dot notation accessible field name and
    value. Useful for looping over model fields in templates.
    """
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Mineral(models.Model):
    name = CharField(max_length=255, unique=True)
    image_filename = CharField(max_length=200, null=True)
    image_caption = TextField(null=True)

    category = CharField(max_length=255, null=True)
    formula = TextField()
    group = CharField(max_length=255, null=True)
    strunz_classification = CharField(max_length=255, null=True)
    color = CharField(max_length=255, null=True)
    crystal_system = CharField(max_length=255, null=True)
    unit_cell = CharField(max_length=255, null=True)
    crystal_symmetry = CharField(max_length=255, null=True)
    cleavage = CharField(max_length=255, null=True)
    mohs_scale_hardness = CharField(max_length=255, null=True)
    luster = CharField(max_length=255, null=True)
    streak = CharField(max_length=255, null=True)
    diaphaneity = CharField(max_length=255, null=True)
    optical_properties = CharField(max_length=255, null=True)
    refractive_index = CharField(max_length=255, null=True)
    crystal_habit = CharField(max_length=255, null=True)
    specific_gravity = CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    @property
    def display_fields(self):
        """
        Returns ordered list of fields with dot notation accessible names and
        values. Excludes fields with null values.
        """
        names = [
            'category', 'group', 'formula', 'strunz classification',
            'crystal system', 'mohs scale hardness', 'luster', 'color',
            'specific gravity', 'cleavage', 'diaphaneity',
            'crystal habit', 'streak', 'optical properties',
            'refractive index', 'unit cell', 'crystal symmetry'
        ]
        values = [
            self.category, self.group, self.formula, self.strunz_classification,
            self.crystal_system, self.mohs_scale_hardness, self.luster, self.color,
            self.specific_gravity, self.cleavage, self.diaphaneity,
            self.crystal_habit, self.streak, self.optical_properties,
            self.refractive_index, self.unit_cell, self.crystal_symmetry
        ]
        fields = list(zip(names, values))

        return [DisplayField(name, value) for (name, value) in fields if value]
