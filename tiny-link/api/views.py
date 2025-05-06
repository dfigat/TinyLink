from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import redirect
from django.http import JsonResponse

from .models import Link
from .serializers import *
from .config import number_of_days, code_length

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
      "http://link.cbpio.pl:8080/api/v1.0/test"
    ])

@api_view(['POST'])
def create_tiny_link(request):
    data = request.data
    serializer_tiny = TinyUrlSerializerCreate(data=data)

    if not serializer_tiny.is_valid():
        return Response(serializer_tiny.errors, status.HTTP_400_BAD_REQUEST)

    link_tiny = serializer_tiny.save()
    final_serializer = TinyUrlSerializer(link_tiny)
    return Response(final_serializer.data, status.HTTP_201_CREATED)

@api_view(['GET'])
def redirect_by_short_code(request, code):
    try:
        link = Link.objects.get(code=code)
        return redirect(link.long_link)
    except Link.DoesNotExist:
        
        return Response({'error': 'tinyLink not found :c'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def show_all_records(request):
    data = Link.objects.all()
    serializer = TinyUrlSerializer(data, many = True)
    return Response(
        serializer.data   
    )

@api_view(['GET'])
def show_configuration(request):
    data = {
        "number_of_days":number_of_days,
        "code_length":code_length
        }
    
    return Response(
        data
    )
@api_view(['GET'])
def show_code(request, long_link):
    try:
        data = Link.objects.get(long_link=long_link)
        return Response(
            data.code
        )
    except Link.DoesNotExist:
        return Response({'error':'tinyLink does not exist :C'}, status=status.HTTP_404_NOT_FOUND)