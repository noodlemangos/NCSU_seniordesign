"""
.. class:: EntrySerializer
    :synopsis: Serializer for the entry data objects

.. moduleauthor:: Will James
"""

from rest_framework import serializers
from entries.models import Entry

class EntrySerializer(serializers.HyperlinkedModelSerializer):
    """
    EntrySerializer class.
    """

    class Meta:
        model = Entry
        fields = ('url','id', 'date_time', 'workload_model', 'command', 'runtime', 'processor', 'memory', 'os_version', 'disk_storage', 'package_versions')
        extra_kwargs = {
            'url': {
                'view_name': 'entries:entry-detail',
            }
        }