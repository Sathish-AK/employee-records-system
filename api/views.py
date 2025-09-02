from rest_framework import viewsets, permissions
from formbuilder.models import FormSchema
from employees.models import EmployeeRecord
from .serializers import FormSchemaSerializer, EmployeeRecordSerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, FormSchema):
            return obj.owner == request.user
        if isinstance(obj, EmployeeRecord):
            return obj.created_by == request.user
        return False

class FormSchemaViewSet(viewsets.ModelViewSet):
    serializer_class = FormSchemaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return FormSchema.objects.filter(owner=self.request.user)

class EmployeeRecordViewSet(viewsets.ModelViewSet):
    serializer_class = EmployeeRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return EmployeeRecord.objects.filter(created_by=self.request.user)
