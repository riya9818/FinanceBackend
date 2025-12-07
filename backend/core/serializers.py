
from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import (Customer,Lead,LeadSource)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
    

# CRM Serializers

class CustomerSerializer(serializers.ModelSerializer):
    account_manager= UserSerializer(read_only=True) #GET
    account_manager_id= serializers.PrimaryKeyRelatedField( #post/put
        queryset=User.objects.all(),
        source="account_manager",
        write_only=True,
        required=False,
        allow_null=True,
    )
    
    class Meta:
        model= Customer
        fields=["id", "name", "email", "joined_date", "is_active", "country",
            "account_manager", "account_manager_id",
        
        ]

class LeadSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model= LeadSource
        fields =["id","name","description"]

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model= Lead
