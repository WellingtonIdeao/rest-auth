from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from rest_framework.authtoken.views import obtain_auth_token
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    # return or create authentication token
    path('api-token-auth/', obtain_auth_token),
]