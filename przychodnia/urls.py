from django.conf import settings
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_owner/', views.add_owner),
    path('show_owners/', views.show_owners),
    path('show_animals/', views.show_animals),
    path('show_bills/', views.show_bills),
    path('watch_owner/', views.watch_owner),
    path('download_bills/', views.download_bills),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)