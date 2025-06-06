from rest_framework import serializers

from .models import Link, APIKey

class TinyUrlSerializer(serializers.ModelSerializer):
    long_link = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ['long_link', 'code', 'lastUsed']

    def get_long_link(self, obj):
        return obj.get_long_link()
    

class TinyUrlSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['long_link']

# class APIKeySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = APIKey
#         fields = ['key', 'name', 'is_active', 'created_at']
#         extra_kwargs = {
#             'key': {'write_only': True},
#             'created_at': {'read_only': True}
#         }