from django.contrib import admin

from .models import *
# Register your models here.

class BankDataAdmin(admin.ModelAdmin):
	list_display = ["bank_id", "bank_name"]

admin.site.register(BankData, BankDataAdmin)

class BranchDataAdmin(admin.ModelAdmin):
	list_display = ["ifsc","bank_id","branch","address","city","district","state"]

admin.site.register(BranchData, BranchDataAdmin)