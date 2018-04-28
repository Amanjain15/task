from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.template import Context
from django.template.loader import get_template

from .models import *

from django.http import JsonResponse,HttpResponse
from django import forms
import csv
import datetime


# Create your views here.
@csrf_exempt
def import_branch(request):
	rows=[]
	bank_set= BankData.objects.all()
	response={}
	try:		
		with open("./media/bank_branch.csv", 'r') as csvfile:
			csvreader = csv.reader(csvfile)
			for row in csvreader:
				rows.append(row)
				# 38434 , 38785, 40000
		print datetime.datetime.now()
		for row in rows[44169:]:
			ifsc=str(row[0])
			bank_id=row[1]
			branch=str(row[2])
			address=str(row[3])
			city=str(row[4])
			district=str(row[5])
			state=str(row[6])

			try:
				bank_obj=BankData.objects.get(bank_id=int(bank_id))
			except Exception as e:
				print bank_id
				raise
			try:
				BranchData.objects.create(
					ifsc=row[0],
					bank_id=bank_obj,
					branch=row[2],
					address=row[3],
					city=row[4],
					district=row[5],
					state=row[6],
				)
				print bank_id,ifsc
			except Exception as e:
				print e,"Exception in saving ",bank_id
	except Exception as e:
		raise
	print datetime.datetime.now
	return JsonResponse(response)

@csrf_exempt
def get_details(request):
	
	if request.method == 'POST':	
		ifsc=str(request.POST.get('ifsc'))
		bank_name=str(request.POST.get('bank_name'))
		branch=str(request.POST.get('branch'))
		address=str(request.POST.get('address'))
		city=str(request.POST.get('city'))
		district=str(request.POST.get('district'))
		state=str(request.POST.get('state'))
		print city,bank_name,ifsc		
		Json={}
		branch_list=[]
		try:
			if ifsc != None and ifsc != "":
				branch_obj=BranchData.objects.get(ifsc=str(ifsc))
				temp=util(branch_obj)
				branch_list.append(temp)
			elif bank_name != None and bank_name != "":
				bank_obj=BankData.objects.get(bank_name=str(bank_name))
				if city != None and city != "":
					# Branches - City Specific
					branch_set=BranchData.objects.filter(city=str(city),bank_id=bank_obj)
					for branch in branch_set:
						temp=util(branch)
						branch_list.append(temp)
				else:
					# All Branches 
					branch_set=BranchData.objects.filter(bank_id=bank_obj)
					for branch in branch_set:
						temp=util(branch)
						branch_list.append(temp)
			Json["success"]=True
			Json["branch_set"]=branch_list
		except Exception as e:
			print str(e)
			Json["success"]=False
			Json["message"]="Error occured due to : " + str(e)
		template = get_template("./table.html")
		context=Context(Json)
		html=template.render(Json)
		return HttpResponse(html)
	elif request.method == 'GET' :
		template = get_template("./detail.html")
		html=template.render()
		return HttpResponse(html)

def util(branch_obj):
	temp={}
	temp['ifsc']=branch_obj.ifsc
	temp['bank_id']=branch_obj.bank_id.bank_id
	temp['branch']=branch_obj.branch
	temp['address']=branch_obj.address
	temp['city']=branch_obj.city
	temp['district']=branch_obj.district
	temp['state']=branch_obj.state
	temp['bank_name']=branch_obj.bank_id.bank_name
	return temp
	pass