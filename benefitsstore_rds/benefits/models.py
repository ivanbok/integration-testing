from django.contrib.auth.models import AbstractUser
from django.db import models

# Product Categories (e.g. Healthcare, Loans etc)
class Categories(models.Model):
    category = models.CharField(max_length=64)

# Individual Listings
class Benefits(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length = 1000)
    category = models.ForeignKey(to='Categories', on_delete=models.CASCADE, blank=True, related_name='benefitsList')
    posted_by = models.ForeignKey(to='BenefitsProviderUser', on_delete=models.CASCADE, blank=True, related_name='postedBenefits')
    provider = models.ForeignKey(to='BenefitsProviderCompany', on_delete=models.CASCADE, blank=True, related_name='benefitsList')
    price = models.IntegerField()
    numberPurchased = models.IntegerField()
    imageurl = models.URLField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.TextField(max_length = 1000, blank=True)
    is_active = models.BooleanField(default=False)
    is_product = models.BooleanField(default=False)

# Companies subscribed to the service
class Company(models.Model):
    company_name = models.CharField(max_length=64)
    standard_points = models.IntegerField(blank=True) # The standard number of points given to each user from the company
    validEmployeeIDList = models.TextField(blank=True) # Uploaded List of Valid Employee IDs that have not been registered as accounts
    validEmployeeIDList_Used = models.TextField(blank=True) # Move Employee ID to this section once they have registered an account
    subscriptionStatus = models.BooleanField(default=True)

# Companies offering their benefits for sale
class BenefitsProviderCompany(models.Model):
    company_name = models.CharField(max_length=64)

# Standard User Account, which indicates the type of user
class User(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)
    is_serviceprovider = models.BooleanField(default=False)
    is_ownstaff = models.BooleanField(default=False)

# Employee Database
class EmployeeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employeeID = models.CharField(max_length=64)
    addressLineOne = models.CharField(max_length=255, blank=True)
    addressLineTwo = models.CharField(max_length=255, blank=True)
    postalcode = models.CharField(max_length=16, blank=True)
    company = models.ForeignKey(to='Company', on_delete=models.CASCADE, blank=True, related_name='employees')
    points = models.IntegerField()
    cart = models.CharField(max_length=255, blank=True)
    benefits = models.CharField(max_length=255, blank=True)

# HR User Database (each company can have multiple HR accounts)
class BusinessUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(to='Company', on_delete=models.CASCADE, blank=True, related_name='HRaccounts')

# Service Provider Accounts Database (each company can have multiple accounts)
class BenefitsProviderUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    serviceCompany = models.ForeignKey(to='BenefitsProviderCompany', on_delete=models.CASCADE, blank=True, related_name='serviceProviderAccounts')

# Own Staff Account
class InternalStaffUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    positionTitle = models.CharField(max_length=64)
    businessFunction = models.CharField(max_length=64)
    admin = models.BooleanField(default=False)

# Transaction History (Active)
class TransactionHistory(models.Model):
    listingID = models.ForeignKey(to = 'Benefits', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    buyer = models.ForeignKey(to = 'EmployeeUser', on_delete=models.CASCADE)
    buyerCompany = models.ForeignKey(to = 'Company', on_delete=models.CASCADE)
    seller = models.ForeignKey(to = 'BenefitsProviderCompany', on_delete=models.CASCADE)
    addressLineOne = models.CharField(max_length=255, blank=True)
    addressLineTwo = models.CharField(max_length=255, blank=True)
    postalcode = models.CharField(max_length=16, blank=True)
    transactionDateTime = models.DateTimeField(auto_now_add=True)

# Redemption History
class RedemptionHistory(models.Model):
    listingID = models.ForeignKey(to = 'Benefits', on_delete=models.CASCADE)
    quantityRedeemed = models.IntegerField()
    buyer = models.ForeignKey(to = 'EmployeeUser', on_delete=models.CASCADE)
    buyerCompany = models.ForeignKey(to = 'Company', on_delete=models.CASCADE)
    seller = models.ForeignKey(to = 'BenefitsProviderCompany', on_delete=models.CASCADE)
    redemptionDateTime = models.DateTimeField(auto_now_add=True)

# Cart Item model for serializer. Not used in actual database
class CartItem(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length = 1000)
    quantity = models.IntegerField()
    category = models.ForeignKey(to='Categories', on_delete=models.CASCADE, blank=True)
    posted_by = models.ForeignKey(to='BenefitsProviderUser', on_delete=models.CASCADE, blank=True)
    provider = models.ForeignKey(to='BenefitsProviderCompany', on_delete=models.CASCADE, blank=True)
    price = models.IntegerField()
    numberPurchased = models.IntegerField()
    imageurl = models.URLField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.TextField(max_length = 1000, blank=True)
    is_active = models.BooleanField(default=False)
    is_product = models.BooleanField(default=False)