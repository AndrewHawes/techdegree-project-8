from django.shortcuts import reverse
from django.test import TestCase

from minerals.models import Mineral, DisplayField
from minerals.templatetags.mineral_filters import base_name

mineral_names = [
    'Arkhamite',
    'Azraelite',
    'Alfredite',
    'Ambienite',
    'Gordonite',
    'Gothamite',
    'Kalelite',
    'Kryptonite',
    'Karaite',
    'Zorelite',
]


def create_mineral(
        name,
        all_fields=True,
        image_filename='test.jpg',
        image_caption='caption test',
        group='group test',
        category='category test',
        formula='formula test',
        strunz_classification='strunz test',
        crystal_system='crystal system test',
        unit_cell='unit cell test',
        color='color test',
        crystal_symmetry='crystal symmetry test',
        cleavage='cleavage test',
        mohs_scale_hardness='mohs scale hardness test',
        luster='luster test',
        streak='streak test',
        diaphaneity='diaphaneity test',
        optical_properties='optical properties test',
        refractive_index='refractive index test',
        crystal_habit='crystal_habit test',
        specific_gravity='specific gravity test'
):
    if all_fields:
        return Mineral.objects.create(
            name=name,
            image_filename=image_filename,
            image_caption=image_caption,
            category=category,
            formula=formula,
            strunz_classification=strunz_classification,
            crystal_system=crystal_system,
            unit_cell=unit_cell,
            color=color,
            crystal_symmetry=crystal_symmetry,
            cleavage=cleavage,
            mohs_scale_hardness=mohs_scale_hardness,
            luster=luster,
            streak=streak,
            diaphaneity=diaphaneity,
            optical_properties=optical_properties,
            refractive_index=refractive_index,
            crystal_habit=crystal_habit,
            specific_gravity=specific_gravity,
            group=group
        )
    else:
        return Mineral.objects.create(
            name='name',
            image_filename=image_filename,
            image_caption=image_caption,
            category='category test limited fields',
            formula='formula test limited fields'
        )


class ModelsTests(TestCase):
    def test_display_field_class(self):
        """
        DisplayField returns fields with dot notation accessible field name
        and value.
        """
        gothamite = create_mineral('Gothamite')
        field = DisplayField('formula', gothamite.formula)
        self.assertEqual(field.name, 'formula')
        self.assertEqual(field.value, 'formula test')

    def test_mineral_model_display_fields_all_fields(self):
        """
        Mineral model's display_fields returns list of fields with field names
        and values accessible by dot notation.
        """
        gothamite = create_mineral('Gothamite')
        fields = gothamite.display_fields
        self.assertEqual(len(fields), 17)
        self.assertEqual(fields[4].name, 'crystal system')
        self.assertEqual(fields[4].value, 'crystal system test')

    def test_mineral_model_display_fields_not_all_fields(self):
        """
        Mineral model's display_fields excludes fields without a value.
        """
        gothamite = create_mineral('Gothamite', all_fields=False)
        fields = gothamite.display_fields
        self.assertEqual(len(fields), 2)
        self.assertEqual(fields[0].name, 'category')
        self.assertEqual(fields[0].value, 'category test limited fields')
        self.assertEqual(fields[1].name, 'formula')
        self.assertEqual(fields[1].value, 'formula test limited fields')


class IndexViewTests(TestCase):
    def setUp(self):
        create_mineral('Gothamite')
        create_mineral('Kryptonite')

    def test_mineral_list(self):
        """Index view's queryset is equal to list of created minerals."""
        response = self.client.get(reverse('minerals:index'))
        self.assertQuerysetEqual(
            response.context['mineral_list'],
            ['<Mineral: Gothamite>', '<Mineral: Kryptonite>'],
            ordered=False
        )

    def test_display_minerals(self):
        """Created minerals are listed on the index page."""
        response = self.client.get(reverse('minerals:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Gothamite')
        self.assertContains(response, 'Kryptonite')


class DetailViewTests(TestCase):
    def test_no_wrap(self):
        """
        Display template splits mineral names with multiple variants to prevent
        wrapping on hyphen.
        """
        mineral = create_mineral("Gothamite-(Y), Gothamite-(Ce), Gothamite-(Nd)")
        url = reverse('minerals:detail', args=(mineral.id,))
        response = self.client.get(url)
        self.assertContains(response, 'white-space: nowrap;')

    def test_detail_display_all_fields(self):
        mineral = create_mineral("Gothamite")
        url = reverse('minerals:detail', args=(mineral.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Crystal Habit')

    def test_detail_display_not_all_fields(self):
        mineral = create_mineral("Gothamite", all_fields=False)
        url = reverse('minerals:detail', args=(mineral.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Formula')
        self.assertNotContains(response, 'Crystal Habit')


class RandomMineralViewTests(TestCase):
    def setUp(self):
        for mineral_name in mineral_names:
            create_mineral(mineral_name)

    def test_random_mineral_redirects(self):
        """Random mineral returns existing mineral."""
        response = self.client.get(reverse('minerals:random_mineral'))
        self.assertEqual(response.status_code, 302)


class SingleParameterSearchViewTests(TestCase):
    def setUp(self):
        for mineral_name in mineral_names:
            create_mineral(mineral_name)

    def test_search_name_single_result(self):
        query = 'krypt'
        url = reverse('minerals:search')
        context = {'query': query}
        response = self.client.get(url, context)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['mineral_list'],
            ['<Mineral: Kryptonite>'],
        )

    def test_search_name_multiple_results(self):
        query = 'nite'
        url = reverse('minerals:search')
        context = {'query': query}
        response = self.client.get(url, context)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['mineral_list'],
            ['<Mineral: Ambienite>',
             '<Mineral: Gordonite>',
             '<Mineral: Kryptonite>'],
            ordered=False
        )

class MultiParameterSearchViewTests(TestCase):
    def setUp(self):
        create_mineral('Arkhamite', group='Silicates', color='greenish blue')
        create_mineral('Kalelite', category='Silicate', luster='Brilliant')
        create_mineral('Gothamite', group='Arsenates', color='reddish orange, crimson')
        create_mineral('Kryptonite', group='Other', color='Usually green or red.')
        create_mineral('Robinite', image_caption='A very silly looking mineral.')

    def test_search_single_result(self):
        context = {'query': 'Kryp', 'all_fields': True}
        url = reverse('minerals:search')
        response = self.client.get(url, context)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['mineral_list'],
            ['<Mineral: Kryptonite>'],
        )

    def test_search_multiple_results(self):
        context = {'query': 'Sil', 'all_fields': True}
        url = reverse('minerals:search')
        response = self.client.get(url, context)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['mineral_list'],
            ['<Mineral: Arkhamite>',
             '<Mineral: Kalelite>',
             '<Mineral: Robinite>'],
            ordered=False
        )

    def test_search_no_results(self):
        context = {'query': 'Revenge!!', 'all_fields': True}
        url = reverse('minerals:search')
        response = self.client.get(url, context)
        self.assertEqual(response.status_code, 200)
        mineral_list = response.context['mineral_list']
        self.assertEqual(mineral_list.count(), 0)


class LetterFilterViewTests(TestCase):
    def setUp(self):
        for mineral_name in mineral_names:
            create_mineral(mineral_name)

    def test_filter_a(self):
        url = reverse('minerals:letter_filter', args=('A',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        mineral_list = response.context['mineral_list']
        for mineral_name in mineral_list:
            self.assertTrue(mineral_name.name.startswith('A'))

    def test_filter_z(self):
        url = reverse('minerals:letter_filter', args=('Z',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        mineral_list = response.context['mineral_list']
        for mineral_name in mineral_list:
            self.assertTrue(mineral_name.name.startswith('Z'))

    def test_filter_no_results(self):
        url = reverse('minerals:letter_filter', args=('Q',))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        mineral_list = response.context['mineral_list']
        self.assertEqual(mineral_list.count(), 0)


class PropertyFilterViewTests(TestCase):
    def setUp(self):
        create_mineral('Arkhamite', group='Silicates', color='greenish blue')
        create_mineral('Ambienite', group='Sulfosalts', color='green')
        create_mineral('Gothamite', group='Silicates', color='reddish orange, crimson')
        create_mineral('Kryptonite', group='Other', color='Usually green or red.')

    def test_group_filter_multiple_results(self):
        kwargs = {'property': 'group', 'value': 'Silicates'}
        url = reverse('minerals:property_filter', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['mineral_list'],
            ['<Mineral: Arkhamite>',
             '<Mineral: Gothamite>',
             ],
            ordered=False
        )

    def test_group_filter_single_result(self):
        kwargs = {'property': 'group', 'value': 'Other'}
        url = reverse('minerals:property_filter', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['mineral_list'],
            ['<Mineral: Kryptonite>']
        )

    def test_group_filter_no_results(self):
        kwargs = {'property': 'group', 'value': 'Ambien'}
        url = reverse('minerals:property_filter', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        mineral_list = response.context['mineral_list']
        self.assertEqual(mineral_list.count(), 0)

    def test_color_filter_multiple_results(self):
        kwargs = {'property': 'color', 'value': 'green'}
        url = reverse('minerals:property_filter', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['mineral_list'],
            ['<Mineral: Arkhamite>',
             '<Mineral: Ambienite>',
             '<Mineral: Kryptonite>'
             ],
            ordered=False
        )

    def test_color_filter_single_result(self):
        kwargs = {'property': 'color', 'value': 'orange'}
        url = reverse('minerals:property_filter', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['mineral_list'],
            ['<Mineral: Gothamite>']
        )

    def test_color_filter_no_results(self):
        kwargs = {'property': 'color', 'value': 'Steve'}
        url = reverse('minerals:property_filter', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        mineral_list = response.context['mineral_list']
        self.assertEqual(mineral_list.count(), 0)


class TemplateTagTets(TestCase):

    def test_base_name_no_hyphen(self):
        mineral_name = 'Gothamite-(Y), Gothamite-(Ce), Gothamite-(Nd)'
        mineral_base_name = base_name(mineral_name)
        self.assertEqual(mineral_base_name, 'Gothamite')

    def test_base_name_with_hyphen(self):
        mineral_name = 'Fluor-uvite-(Y), Fluor-uvite-(Hello)'
        mineral_base_name = base_name(mineral_name)
        self.assertEqual(mineral_base_name, 'Fluor-uvite')







