from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
import config.settings.base as config
from users.permissions import IsEditor

User = get_user_model()

class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class UserMe(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """

    permission_classes = [IsEditor]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        user = User.objects.filter(username=request.user).first()
        if user is None:
            raise NotFound(detail="User not found", code=404)
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data)
            