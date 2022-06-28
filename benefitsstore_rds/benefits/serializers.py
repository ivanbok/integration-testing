from rest_framework import serializers

# Register your models here.
from .models import Categories, Benefits, Company, BenefitsProviderCompany, User, EmployeeUser, \
    BusinessUser, BenefitsProviderUser, InternalStaffUser, TransactionHistory, RedemptionHistory, CartItem

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id','category']

class BenefitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefits
        fields = ['id', 'title', 'description', 'category', 'posted_by', 'provider', 'price', 'numberPurchased', 'imageurl',
            'date_created', 'date_created', 'tags', 'is_active', 'is_product']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'company_name','standard_points','validEmployeeIDList','validEmployeeIDList_Used',
        'subscriptionStatus']

class BenefitsProviderCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = BenefitsProviderCompany
        fields = ['id', 'company_name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_employee', 'is_business', 'is_serviceprovider', 'is_serviceprovider', 'is_ownstaff']

class EmployeeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeUser
        fields = ['id', 'user','employeeID','addressLineOne','addressLineTwo','postalcode','company',
            'points','cart','benefits']

class BusinessUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUser
        fields = ['id', 'user','company']

class BenefitsProviderUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BenefitsProviderUser
        fields = ['id', 'user','serviceCompany']

class InternalStaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalStaffUser
        fields = ['id', 'user','positionTitle','businessFunction','admin']

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = ['id', 'listingID','quantity','price','buyer','buyerCompany','seller',
            'addressLineOne','addressLineTwo','postalcode','transactionDateTime']

class RedemptionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RedemptionHistory
        fields = ['id', 'listingID','quantityRedeemed','buyer','buyerCompany','seller','redemptionDateTime']

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['title' ,'description', 'quantity', 'category', 'posted_by', 'provider', 'price', 'numberPurchased', 'imageurl',
            'date_created', 'date_created', 'tags', 'is_active', 'is_product']
