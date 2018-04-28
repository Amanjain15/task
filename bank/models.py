from __future__ import unicode_literals

from django.db import models

# Create your models here.
class BankData(models.Model):
	bank_id=models.IntegerField(primary_key=True)
	bank_name=models.CharField(max_length=255)
	def __unicode__(self):
		return str(self.bank_id)
	def __str__(self):
		return str(self.bank_id)

class BranchData(models.Model):
	ifsc=models.CharField(max_length=255, unique=True) 
	bank_id=models.ForeignKey("BankData",db_column="bank_id")
	branch=models.CharField(max_length=255)
	address=models.CharField(max_length=255)
	city=models.CharField(max_length=255)
	district=models.CharField(max_length=255)
	state=models.CharField(max_length=255)
	def __unicode__(self):
		return self.branch
	def __str__(self):
		return self.branch