"""
data_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

@author Will James
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from data_api import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title='Data API', description='RESTful API for AIXPRT data entries')),
    url(r'^$', views.api_root),
    url(r'^', include(('entries.urls', 'entries'), namespace='entries')),
]
