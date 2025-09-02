from django.db import models
from django.contrib.auth.models import User

class FormSchema(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    # JSON structure: [{"name":"emp_id","label":"Employee ID","type":"number","required":true}, ...]
    fields = models.JSONField(default=list)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forms")

    def __str__(self):
        return self.name
