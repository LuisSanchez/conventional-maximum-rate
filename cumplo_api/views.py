import requests
import json
import locale
import datetime
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from webapp.models import Credit
from external_api.views import TMCByYearAndMonth, TodayUF

_locale_decimal = locale.localeconv()['decimal_point']
_locale_thousands = locale.localeconv()['thousands_sep']

def replace_chilean_decimals(num):
    """ For some reason globalization on my computer is not working
        cant use locales, so I had to do this... terrible """
    if _locale_decimal == '.':
        num = num.replace('.', '') # replace thousands
        num = num.replace(',', '.') # sets decimals
    return float(num)

def calculate_pesos_using_uf(monto_uf, todayUF):
    """ Pesos with the UF of the day """
    pesos_amount = abs(monto_uf * todayUF)
    return int(pesos_amount)

def calculate_tmc_by_given_day(credit: Credit, total_value, rate):
    """ Calcule of the tmc """
    # days to multiply the tmc (dias de mora totales)
    days_of_tmc = credit.payment_day_with_calculated_tmc - credit.payment_deadline_days
    # value of the total multiplied by the percentage of the debt rate
    total_value = abs((total_value * rate) / 100)
    # amount to pay is calculated dividing the total of days of the month multiplied by the tmc days
    total_value = (total_value / 30) * days_of_tmc
    return int(total_value)


class CalculateTMCForCredit(APIView, Credit):
    """ Calculates the tmc for the given credits on the given day after the deadline """
    def post(request, credit: Credit, format=None):
        dt = datetime.datetime.today()
        kwargs = { 
            'year': dt.year, 
            'month': dt.month 
        }
        res_tmc = TMCByYearAndMonth.get(request, None, kwargs=kwargs)

        todayUF = TodayUF.get(request)
        todayUF = todayUF.data['UFs'][0]["Valor"]
        valorUF = replace_chilean_decimals(todayUF)

        pesos_amount = calculate_pesos_using_uf(credit.monto_uf, valorUF)
        tmc = calculate_tmc_by_given_day(credit, pesos_amount, 28.2)

        result = { 
            "total_value": pesos_amount,
            "tmc": tmc
        }

        return Response(json.dumps(result))
