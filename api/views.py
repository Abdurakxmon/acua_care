from django.shortcuts import render
# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import RegisterSerializer


# {
#     "first_name":"first_name",
#     "last_name":"last_name",
#     "email":"email@ew.wq",
#     "password":"password",
#     "profile":{
#         "phone":"phone",
#         "address":"address"
#     }
# }


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def post(self, request):
        print(request.user)
        return Response({"message": "This is a protected endpoint, accessible only to authenticated users."})
