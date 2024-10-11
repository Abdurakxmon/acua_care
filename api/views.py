from django.shortcuts import render
# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from datetime import datetime


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
        ls = [
            'daily',
            'number_of_people',
            'number_of_rakvina',
            'having_bath',
            'cooking',
            'laundry',
            'washing_dishes'
        ]

        # [
        #   'daily': 1  ,
        #   'number_of_rakvina':3,
        #   'number_of_people' : 1,
        # 	'number_of_rakvina' : 2,
        # 	'having_bath' : ['7:30','20:00'],
        # 	'cooking' : ['12:30','18:00'],
        # 	'laundry' : ['12:30','18:00'],
        # 	'washing_dishes' : ['13:30','19:00']
        # ]

        data = request.data
        for i in ls:
            if i not in data:
                return Response({"message": f"{i} field is required!"},status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "This is a protected endpoint, accessible only to authenticated users."})
    # print( datetime.now().date())
