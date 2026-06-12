from rest_framework import serializers

from .models import Group
from django.contrib.auth.models import User

class SplitInputSerializer(serializers.Serializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    
class ExpenseCreationSerializer(serializers.Serializer):
    group_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    currency = serializers.CharField(max_length=5)
    splits = SplitInputSerializer(many=True)
