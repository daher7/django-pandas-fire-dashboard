from django.urls import path
from analysis import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('estadisticas/', views.mostrar_estadisticas, name = 'estadisticas'),
    path('mapa/', views.mostrar_mapa, name = 'mapa'),
    path('metodologia/', views.mostrar_metodologia, name = 'metodologia')
]
