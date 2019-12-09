"""
entries URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

@author Will James
"""

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from entries import views

urlpatterns = [
    url(r'^entries/$', views.EntryList.as_view(), name='entry-list'),
    url(r'^entries/(?P<pk>[0-9]+)/$', views.EntryDetail.as_view(), name='entry-detail'),
]