from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from torch import float16
from .test_api import api_function

class data_api(APIView):
   def get(self,request):
      response = {}
      Price_per_promo=request.GET.get('Price_per_promo')
      lower_guardrail=request.GET.get('lower_guardrail')
      upper_guardrail=request.GET.get('upper_guardrail')
      Incremental_Spend=request.GET.get('Incremental_Spend')
      Step_size=request.GET.get('Step_size')
      print(Price_per_promo,lower_guardrail,upper_guardrail,Incremental_Spend,Step_size)
      result=api_function(float(Price_per_promo),float(lower_guardrail),float(upper_guardrail),float(Incremental_Spend),float(Step_size))
      print(result)
      json_records = result.to_json(orient ='records')
      print(json_records)
      return Response({"msg" : "success", "data" : json_records})

   

# Create your views here.
#http://127.0.0.1:8000/data_api/test-api/?Price_per_promo=80&lower_guardrail=0.3&upper_guardrail=0.3&Incremental_Spend=1000000&Step_size=1