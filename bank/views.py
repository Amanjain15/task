from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import *

from django.http import JsonResponse,HttpResponse
from django import forms
import csv
import datetime

# Create your views here.
class UploadFileForm(forms.Form):
	file = forms.FileField()

@csrf_exempt
def import_details(request):
	try:
		if request.method == "POST":
			form = UploadFileForm(request.POST,request.FILES)
			if form.is_valid():
				request.FILES['file'].save_to_database(model=BranchData,mapdict=["ifsc","bank_id","branch","address","city","district","state"])
				return HttpResponse("OK")
			else:
				return HttpResponseBadRequest()
		else:
			form = UploadFileForm()
			return render(request,'upload.html',{'form':form ,'msg':"Upload table"})
	except Exception as e:
		print str(e);
		return HttpResponse("Page not found")

	return HttpResponse("<H1>404 PAGE NOT FOUND</H1>")

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
		for row in rows[40001:50000]:
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
		ifsc=request.POST.get('ifsc')
		bank_name=request.POST.get('bank_id')
		branch=request.POST.get('branch')
		address=request.POST.get('address')
		city=request.POST.get('city')
		district=request.POST.get('district')
		state=request.POST.get('state')
		response=[]
		if ifsc != "":
			branch_obj=BranchData.objects.get(ifsc=ifsc)
			bank_obj=BankData.objects.get(bank_name=bank_name)
			temp={}
			temp['ifsc']=branch_obj.ifsc
			temp['bank_id']=bank_obj.bank_id
			temp['branch']=branch_obj.branch
			temp['address']=branch_obj.address
			temp['city']=branch_obj.city
			temp['district']=branch_obj.district
			temp['state']=branch_obj.state
			temp['bank_name']=bank_obj.bank_name
			response.append(temp)
		elif bank_name != "":
			bank_obj=BankData.objects.get(bank_name=bank_name)
			if city != "":
				branch_set=BranchData.objects.filter(city=city,bank_id=bank_obj)
				for branch in branch_set:
					temp={}
					temp['ifsc']=branch_set.ifsc
					temp['bank_id']=bank_set.bank_id
					temp['branch']=branch_set.branch
					temp['address']=branch_set.address
					temp['city']=branch_set.city
					temp['district']=branch_set.district
					temp['state']=branch_set.state
					temp['bank_name']=bank_set.bank_name
					response.append(temp)
		
		return JsonResponse(response)
	elif request.method == 'GET' :
		response=[]


		return response
		