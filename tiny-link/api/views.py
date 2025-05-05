from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def api_default(request):
    return Response([
        "http://link.cbpio.pl:8080/api/v1.0/"
    ])
@api_view(['GET'])
def api_v1_0(request):
    return Response([
      "http://link.cbpio.pl:8080/api/v1.0/short",
      "http://link.cbpio.pl:8080/api/v1.0/long"
    ])