from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.shortcuts import redirect
from django.db.utils import IntegrityError
from dotenv import load_dotenv
from os import getenv

from django.utils.timezone import now
from datetime import timedelta

from .models import Link
from .serializers import *
from .config import number_of_days, code_length, THRESHOLD, API_VERSION
from .utils import validate_api_key

from django_ratelimit.decorators import ratelimit
from django_ratelimit.core import is_ratelimited

load_dotenv('../tinyLink/.env')
API_URL = getenv('API_URL')
API_URL_SHORTENED = getenv('API_URL_SHORTENED')
WEB_KEY = getenv('WEB_KEY')

# Create your views here.
@api_view(['GET'])
def api_default(request):
    return Response([
        f"{API_URL}{API_VERSION}"
    ])

@api_view(['GET'])
def api_v1_0(request):
    return Response([
      f"{API_URL}{API_VERSION}/short",
      f"{API_URL}{API_VERSION}/test"
    ])

@api_view(['POST'])
# @ratelimit(key='ip', rate='1/m')
@permission_classes([IsAuthenticated])
def create_tiny_link(request):
    # if request.data.get('x-api-link') == WEB_KEY:
        # if is_ratelimited(request, group='create_tiny_link', key='ip', rate='1/s', method='POST', increment=True):
            # return Response({'error': 'Rate limit exceeded'}, status.HTTP_429_TOO_MANY_REQUESTS)
    
    # is_valid, error = validate_api_key(request)
    # if not is_valid:
    #     return error
    
    if request.user.username == 'demouser':
        if is_ratelimited(request, group='create_tiny_link', key='ip', rate='5/m', method='POST', increment=True):
            return Response({'error': 'Rate limit exceeded'}, status.HTTP_429_TOO_MANY_REQUESTS)
    
    data = request.data
    serializer_tiny = TinyUrlSerializerCreate(data=data)

    already_created = Link.objects.filter(long_link=data['long_link']).first()
    if already_created:
        output_data = TinyUrlSerializer(already_created).data
        output_data = output_data.copy()
        output_data['code'] = API_URL_SHORTENED + output_data['code']
        return Response(output_data, status.HTTP_200_OK)

    if not serializer_tiny.is_valid():
        return Response(serializer_tiny.errors, status.HTTP_400_BAD_REQUEST)
    
    link_tiny = serializer_tiny.save()
    final_serializer = TinyUrlSerializer(link_tiny)
    output_data = final_serializer.data.copy()
    output_data['code'] = API_URL_SHORTENED + output_data['code']
    return Response(output_data, status.HTTP_201_CREATED)

@api_view(['GET'])
def redirect_by_short_code(request, code):
    try:
        link = Link.objects.get(code=code)
        link.last_used = now()
        link.save()
        return redirect(link.long_link)
    except Link.DoesNotExist:
        
        return Response({'error': 'tinyLink not found :c'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def show_all_records(request):
    data = Link.objects.all()
    serializer = TinyUrlSerializer(data, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def count_all_records(request):
    count = Link.objects.all().count()
    return Response({"count": count}, status.HTTP_200_OK)

@api_view(['GET'])
def show_configuration(request):
    data = {
        "number_of_days":number_of_days,
        "code_length":code_length
    }
    
    return Response(data)

@api_view(['GET'])
def show_code(request, long_link):
    try:
        data = Link.objects.get(long_link=long_link)
        return Response(
            data.code
        )
    except Link.DoesNotExist:
        return Response({'error':'tinyLink does not exist :C'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE'])
def delete_all_by_threshold(request, threshold=THRESHOLD):
    threshold = THRESHOLD # For now
    try:
        threshold = int(threshold)
    except ValueError:
        return Response({'error': 'Threshold must be of type integer'}, status.HTTP_400_BAD_REQUEST)

    days = timedelta(days=threshold)
    expiration_time = now() - days
    expired = Link.objects.filter(lastUsed__lt=expiration_time)
    count = expired.count()
    expired.delete()
    return Response({"deleted_count": count}, status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_by_code(request, code):
    to_delete = Link.objects.filter(code=code)
    count = to_delete.count()
    to_delete.delete()
    return Response({"deleted_count": count}, status.HTTP_200_OK)

@api_view(['GET'])
def is_alive(request):
    return Response({"status": "alive"}, status.HTTP_200_OK)


# Temporary
from django.shortcuts import render

def serve_index(request):
    return render(request, 'index.html')

# Regarding jwt token
@api_view(['POST'])
@permission_classes([])
def get_tokens(request):
    view = TokenObtainPairView.as_view()
    return view(request._request)

@api_view(['POST'])
@permission_classes([])
def refresh_token(request):
    view = TokenRefreshView.as_view()
    return view(request._request)
