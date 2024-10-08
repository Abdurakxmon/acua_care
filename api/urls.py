from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .import views

app_name = 'api'


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('protected/',views.ProtectedView.as_view(), name='protected'),
]