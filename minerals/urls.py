from django.urls import path, include

from . import views

app_name = 'minerals'
urlpatterns = [
    path('', views.index, name='index'),
    path('minerals/<int:mineral_id>/', views.detail, name='detail'),
    path('random_mineral/', views.random_mineral, name='random_mineral'),
    path('search/', views.search, name='search'),
    path('letter_filter/<str:letter>/', views.letter_filter, name='letter_filter'),
    path('property_filter/<str:property>/<str:value>/', views.property_filter,
         name='property_filter'),
]
