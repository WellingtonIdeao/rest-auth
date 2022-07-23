from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserLoginView, UserLogoutView
from rest_framework.authtoken.views import obtain_auth_token
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/login/', UserLoginView.as_view(), name='login'),
    path('api-auth/logout/', UserLogoutView.as_view(), name='logout'),
    # return or create authentication token
    path('api-token-auth/', obtain_auth_token),
]