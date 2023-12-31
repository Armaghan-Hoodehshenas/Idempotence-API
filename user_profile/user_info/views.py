from django.core.cache import cache
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . models import *
from . serializers import *

# Create your views here.

class ProfileView(APIView):
    def put(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            key = hash(f"{data}")
            is_exists = cache.get(key)

            if is_exists:
                return Response(data=serializer, status=status.HTTP_200_OK)
            else:
                Profile.objects.create(first_name=data['first_name'], last_name=data['last_name'])
                cache.set(key, 'idem', 20)
                return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)