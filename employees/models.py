from django.db import models
from django.contrib.auth.models import User
from formbuilder.models import FormSchema

class EmployeeRecord(models.Model):
    form = models.ForeignKey(FormSchema, on_delete=models.PROTECT, related_name="employee_records")
    data = models.JSONField(default=dict)  # {field_name: value}
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
