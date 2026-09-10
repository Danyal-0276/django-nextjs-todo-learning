from rest_framework import serializers
from todo.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="srno", read_only=True)

    class Meta:
        model = Todo
        fields = [
            "id",
            "title",
            "completed",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
