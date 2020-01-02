from random import choice

from django.db.models import Q, AutoField
from django.shortcuts import get_object_or_404, render, reverse
from django.http import HttpResponseRedirect

from .models import Mineral


def index(request):
    mineral_list = Mineral.objects.all()
    return render(request, 'minerals/index.html', {'mineral_list': mineral_list})


def detail(request, mineral_id=None):
    mineral = get_object_or_404(Mineral, pk=mineral_id)
    return render(request, 'minerals/detail.html', {'mineral': mineral})


def random_mineral(request):
    mineral_list = Mineral.objects.all()
    mineral = choice(mineral_list)
    return HttpResponseRedirect(reverse('minerals:detail', args=(mineral.id,)))


def search(request):
    search_term = request.GET.get('query')
    all_fields = request.GET.get('all_fields')
    if all_fields:
        fields = [f for f in Mineral._meta.fields if not isinstance(f, AutoField)]
        queries = [Q(**{field.name + '__icontains': search_term}) for field in fields]
        qs = Q()
        for query in queries:
            qs = qs | query
        mineral_list = Mineral.objects.filter(qs)
    else:
        mineral_list = Mineral.objects.filter(name__icontains=search_term)
    return render(request, 'minerals/index.html', {'mineral_list': mineral_list})


def letter_filter(request, letter):
    mineral_list = Mineral.objects.filter(name__startswith=letter)
    context = {'mineral_list': mineral_list, 'active_filter': letter}

    return render(request, 'minerals/index.html', context)


def property_filter(request, property, value):
    query = Q(**{property + '__icontains': value})
    mineral_list = Mineral.objects.filter(query)
    context = {'mineral_list': mineral_list, 'active_filter': value}

    return render(request, 'minerals/index.html', context)
