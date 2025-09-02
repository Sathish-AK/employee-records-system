from rest_framework import serializers
from formbuilder.models import FormSchema
from employees.models import EmployeeRecord

class FormSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormSchema
        fields = ["id","name","description","fields"]

    def create(self, validated_data):
        user = self.context['request'].user
        return FormSchema.objects.create(owner=user, **validated_data)

class EmployeeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeRecord
        fields = ["id","form","data","created_at","updated_at"]
        read_only_fields = ["created_at","updated_at"]

    def create(self, validated_data):
        user = self.context['request'].user
        return EmployeeRecord.objects.create(created_by=user, **validated_data)
