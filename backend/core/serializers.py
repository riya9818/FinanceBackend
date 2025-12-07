
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
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source="customer",
        write_only=True,
        required=False,
        allow_null=True,
    )
    source = LeadSourceSerializer(read_only=True)
    source_id = serializers.PrimaryKeyRelatedField(
        queryset=LeadSource.objects.all(),
        source="source",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Lead
        fields= [
            "id", "title", "status", "created_at", "expected_value", "notes",
            "customer", "customer_id",
            "source", "source_id",
        ]
