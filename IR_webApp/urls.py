from django.contrib import admin
from django.urls import path
from search_engine import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('speech/', views.speech, name='speech'),
]