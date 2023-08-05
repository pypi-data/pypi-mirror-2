# django imports
from django.conf import settings
from django.http import HttpResponse

# import resources
import resources.utils

def create_css(request):
    """
    """
    resources.utils.create_css()
    return HttpResponse("Created CSS")

def create_javascript(request):
    """
    """
    resources.utils.create_javascript()
    return HttpResponse("Created Javascript")
    
def create_resources(request):
    resources.utils.reset()
    resources.utils.create_resources()
    return HttpResponse("Created Resources")
    