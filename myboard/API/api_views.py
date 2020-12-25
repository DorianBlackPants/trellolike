from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from myboard.API.permissions import IsOwnerOrReadOnly, UserRegistration, ReadOnly
from myboard.API.serializers import TaskSerializer, UserSerializer, RegisterSerializer
from myboard.models import Task, Profile


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [BasicAuthentication, ]
    permission_classes = [IsOwnerOrReadOnly | IsAdminUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if request.user.is_superuser or instance.created_by == request.user:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)

        raise PermissionDenied('Not authorized.')

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'list':
            permission_classes = [ReadOnly]
        elif self.action == 'retrieve':
            permission_classes = [ReadOnly]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsOwnerOrReadOnly | IsAdminUser]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class TaskStatusViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [ReadOnly]

    def get_queryset(self):
        queryset = Task.objects.all()
        status = self.request.query_params.get('status', None)
        if status in ['1', '2', '3', '4', '5']:
            queryset = queryset.filter(status=status)
            if queryset.exists():
                return queryset
            raise NotFound('No status objects!')
        raise NotFound('Status not found')


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = Profile.objects.all()
    authentication_classes = [BasicAuthentication, ]
    permission_classes = [IsAdminUser | UserRegistration]

    def get_serializer_class(self):
        if hasattr(self.request, 'method'):
            if self.request.method in SAFE_METHODS:
                return UserSerializer
            elif self.request.method == 'POST':
                return RegisterSerializer
            else:
                return UserSerializer
