from rest_framework.viewsets import ReadOnlyModelViewSet
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView

from .serializers import UserSerializer
from .permissions import ReadOnly


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [ReadOnly]


# Login view
class UserLoginView(LoginView):
    template_name = 'api/registration/login.html'


# Logout view
class UserLogoutView(LogoutView):
    template_name = 'api/registration/logged_out.html'

