"""
Handles the url requests and returns HTTP responses

@author Will James
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
 
@api_view(['GET'])
def api_root(request, format=None):
    """
    Handles the request for the api_root view
    :param request: HTTP Request
    :param format: Option request format
    :return: HTTP response for the entries page
    """
    return Response({
       'entries': reverse('entries:entry-list', request=request, format=format),
})