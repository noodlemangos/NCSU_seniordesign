"""
.. class:: Entry
    :synopsis: Model representation of a AIXPRT data entry

.. moduleauthor:: Will James
"""

from django.db import models

class Entry(models.Model):
    """
    Entry class.

    Args:

        - **date_time** (DateTime): Date/time that data entry is created
        - **workload_model** (string): Tensorflow Github URL to the machine learning model used for the workload run
        - **command** (string): Console command that was executed for the workload run
        - **runtime** (int): Amount of time it took in nanoseconds for the workload to finish running
        - **processor** (string): Name of the processor for the machine that the workload was ran on
        - **memory** (float): The amount of memory in GB for the machine that the workload was ran on
        - **os_version** (string): Name of the operating system for the machine that the workload was ran on
        - **disk_storage** (float): The amount of disk storage in GB for the machine that the workload was ran on
        - **package_versions** (string): A string contatining every installed package on the environment that the workload was ran on
        
    """
    date_time = models.DateTimeField(auto_now_add=True)
    workload_model = models.CharField(max_length=100, blank=False, null=False, default="Not Available")
    command = models.CharField(max_length=400, blank=False, null=False, default="Not Available")
    runtime = models.BigIntegerField(blank=False, null=False, default=0)
    processor = models.CharField(max_length=100, blank=False, null=False, default="Not Available")
    memory = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=0)
    os_version = models.CharField(max_length=100, blank=False, null=False, default="Not Available")
    disk_storage = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=0)
    package_versions = models.TextField(blank=False, null=False, default="Not Available")

    class Meta:
        ordering = ('date_time',)