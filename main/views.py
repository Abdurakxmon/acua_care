from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

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
