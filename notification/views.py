from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from feed.pagination import SimplePagination
from notification.serializers import NotificationSerializer


@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
class NotificationListView(ListAPIView):
    pagination_class = SimplePagination
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return []
        return user.notifications.all()
