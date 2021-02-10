from rest_framework import serializers
from . import models


class TaskSerielizer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = "__all__"

