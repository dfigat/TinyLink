from .models import APIKey
from rest_framework.response import Response
from rest_framework import status

def validate_api_key(request):
    api_key = request.headers.get('X-API-KEY') or request.GET.get('api_key')
    
    if not api_key:
        return False, Response(
            {'error': 'API key required'},
            status.HTTP_401_UNAUTHORIZED
        )
    
    if not APIKey.objects.filter(key=api_key, is_active=True).exists():
        return False, Response(
            {'error': 'Invalid API key'},
            status.HTTP_403_FORBIDDEN
        )
    
    return True, Response({'msg': 'successfully validated'}, status.HTTP_202_ACCEPTED)