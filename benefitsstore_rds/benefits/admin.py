from django.contrib import admin

# Register your models here.
from .models import Categories, Benefits, Company, BenefitsProviderCompany, User, EmployeeUser, \
    BusinessUser, BenefitsProviderUser, InternalStaffUser, TransactionHistory, RedemptionHistory

# Register your models here.
admin.site.register(Categories)
admin.site.register(Benefits)
admin.site.register(Company)
admin.site.register(BenefitsProviderCompany)
admin.site.register(User)
admin.site.register(EmployeeUser)
admin.site.register(BusinessUser)
admin.site.register(BenefitsProviderUser)
admin.site.register(InternalStaffUser)
admin.site.register(TransactionHistory)
admin.site.register(RedemptionHistory)