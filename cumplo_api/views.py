import requests
import json
import locale
import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from webapp.models import Credit
from external_api.views import TMCByYearAndMonth

_locale_decimal = locale.localeconv()['decimal_point']
_locale_thousands = locale.localeconv()['thousands_sep']

def replace_chilean_decimals(num):
    if _locale_decimal == '.':
        num = num.replace('.', '') # replace thousands
        num = num.replace(',', '.') # sets decimals
    return float(num)

# def get_tmc_for_credit(credit or None)
#     return None

class CalculateTMCForCredit(APIView, Credit):
    """ Calculates the tmc for the given credits on the given day after the deadline """
    def post(request, credit: Credit, format=None):
        dt = datetime.datetime.today()
        kwargs = { 
            'year': dt.year, 
            'month': dt.month 
        }
        res_tmc = TMCByYearAndMonth.get(request, None, kwargs=kwargs)

        mock_result = { 
            "credito": credit.monto_uf * 5,
        }

        return Response(json.dumps(mock_result))
