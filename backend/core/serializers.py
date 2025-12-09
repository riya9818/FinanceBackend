
from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import (Card, Customer, ExchangeRate, ExpenseCategory,Lead,LeadSource, Proposal,Project,SalesRegion
                         ,RegionSalesStat, ScheduledPayment, Task, Section, SectionCategory, Transaction, VisitorStat)

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
class ProposalSerializer(serializers.ModelSerializer):
    lead = LeadSerializer(read_only=True)
    lead_id = serializers.PrimaryKeyRelatedField(
        queryset=Lead.objects.all(),
        source="lead",
        write_only=True,
    )
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source="customer",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Proposal
        fields = [
            "id", "sent_date", "status", "amount", "notes",
            "lead", "lead_id",
            "customer", "customer_id",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source="customer",
        write_only=True,
    )
    proposal_id = serializers.PrimaryKeyRelatedField(
        queryset=Proposal.objects.all(),
        source="proposal",
        write_only=True,
        required=False,
        allow_null=True,
    )
    proposal = ProposalSerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            "id", "name", "status",
            "target_revenue", "actual_revenue",
            "start_date", "end_date",
            "customer", "customer_id",
            "proposal", "proposal_id",
        ]

class SalesRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesRegion
        fields = ["id", "name"]


class RegionSalesStatSerializer(serializers.ModelSerializer):
    region = SalesRegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=SalesRegion.objects.all(),
        source="region",
        write_only=True,
    )

    class Meta:
        model = RegionSalesStat
        fields = ["id", "region", "region_id", "month", "year", "amount", "change_percent"]

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="assigned_to",
        write_only=True,
        required=False,
        allow_null=True,
    )
    related_project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        source="related_project",
        write_only=True,
        required=False,
        allow_null=True,
    )
    related_lead_id = serializers.PrimaryKeyRelatedField(
        queryset=Lead.objects.all(),
        source="related_lead",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Task
        fields = [
            "id", "title", "description", "priority",
            "due_date", "is_completed", "created_at",
            "assigned_to", "assigned_to_id",
            "related_project_id", "related_lead_id",
        ]

# ---------- DOCUMENTS ----------

class SectionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionCategory
        fields = ["id", "name"]


class SectionSerializer(serializers.ModelSerializer):
    category = SectionCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=SectionCategory.objects.all(),
        source="category",
        write_only=True,
    )
    reviewer = UserSerializer(read_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="reviewer",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Section
        fields = [
            "id", "title", "section_type", "status",
            "target", "limit", "order_index",
            "category", "category_id",
            "reviewer", "reviewer_id",
        ]

#-----Document

class SectionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionCategory
        fields = ["id", "name"]


class SectionSerializer(serializers.ModelSerializer):
    category = SectionCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=SectionCategory.objects.all(),
        source="category",
        write_only=True,
    )
    reviewer = UserSerializer(read_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="reviewer",
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Section
        fields = [
            "id", "title", "section_type", "status",
            "target", "limit", "order_index",
            "category", "category_id",
            "reviewer", "reviewer_id",
        ]

# ---------- FINANCE ----------

class CardSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Card
        fields = [
            "id", "card_type", "last4",
            "expiry_month", "expiry_year",
            "spending_limit", "available_balance",
            "is_frozen", "user",
        ]
        read_only_fields = ["user"]

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ["id", "name"]
    
class TransactionSerializer(serializers.ModelSerializer):
    card = CardSerializer(read_only=True)
    card_id = serializers.PrimaryKeyRelatedField(
        queryset=Card.objects.all(),
        source="card",
        write_only=True,
    )
    category = ExpenseCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ExpenseCategory.objects.all(),
        source="category",
        write_only=True,
        required=False,
        allow_null=True,
    )
    class Meta:
        model = Transaction
        fields = [
            "id", "title", "description", "amount",
            "currency", "transaction_date", "is_recurring",
            "card", "card_id",
            "category", "category_id",
        ]


class ScheduledPaymentSerializer(serializers.ModelSerializer):
    card = CardSerializer(read_only=True)
    card_id = serializers.PrimaryKeyRelatedField(
        queryset=Card.objects.all(),
        source="card",
        write_only=True,
    )

    class Meta:
        model = ScheduledPayment
        fields = ["id", "title", "amount", "due_date", "card", "card_id"]


class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = [
            "id", "from_currency", "to_currency",
            "rate", "tax_percent", "fee_percent", "updated_at",
        ]

# ---------- ANALYTICS ----------

class VisitorStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorStat
        fields = ["id", "date", "visitor_count"]
