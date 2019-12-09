"""
Retrieves and saves entry data objects and displays it as a view / detailed view

Referenced tutorial at: https://codeburst.io/building-an-api-with-django-rest-framework-and-class-based-views-75b369b30396
@author Will james
"""

from django.shortcuts import render
from entries.models import Entry
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from entries.serializers import EntrySerializer
from django.contrib.auth.decorators import login_required

class EntryList(generics.ListCreateAPIView):
    """
    EntryList class. Uses DjangoRestFramework generics class to create/save a list view of entry data objects.
    """
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    def perform_create(self, serializer):
        """
        Saves a new/updated entry into the database.
        """
        serializer.save()


class EntryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    EntryDetail class. Uses DjangoRestFramework generics class to retrieve a list entry data objects.
    """
    serializer_class = EntrySerializer

    def get_queryset(self):
        """
        Retrieves all of the entry data objects
        :return: All of the entry data objects
        """
        return Entry.objects.all()