import requests
import json
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from web_project import settings


def get_json_from_UF_response(res):
    """ The api returns 200 even if there is an error... 
        this is a temporary workaround"""
    try:
        return res.json()
    except:
        res = {
            "UFs": [
                {
                "Valor": "28.664,65",
                "Fecha": "2020-08-15"
                }
            ]
        }
        return res

def get_json_from_TMC_response(res):
    """ The api returns 200 even if there is an error... 
        this is a temporary workaround"""
    try:
        return res.json()
    except:
        res = {
            "TMCs": [
                {
                "Titulo": "Operaciones no reajustables en moneda nacional de menos de 90 días",
                "SubTitulo": "Inferiores o iguales al equivalente de 5.000 unidades de fomento",
                "Valor": "35.04",
                "Fecha": "2020-08-14",
                "Tipo": "26"
                },
                {
                "Titulo": "Operaciones no reajustables en moneda nacional de menos de 90 días",
                "SubTitulo": "Superiores al equivalente de 5.000 unidades de fomento",
                "Valor": "6.81",
                "Fecha": "2020-08-14",
                "Tipo": "25"
                },
            ]
        }
        return res


class TodayUF(APIView):
    """ Retrieve the UF of the day """
    def get(self, request, *args):
        url = '%s/uf?apikey=%s&formato=json' % ('https://api.sbif.cl/api-sbifv3/recursos_api', '6ee9263b4d5b8b76adb291bfb6ba03f1563a9d14')
        res = requests.get(url)
        res = get_json_from_UF_response(res)
        return Response(res)

class TMCByYearAndMonth(APIView):
    """ Retrieve the TMC year and month """
    def get(self, request, *args, **kwargs):
        if kwargs.get('year', None) == None:
            kwargs = kwargs['kwargs']
        tmc_year = kwargs['year']
        tmc_month = kwargs['month']
        url = '%s/tmc/%s/%s?apikey=%s&formato=json' % (settings.URL_SBIF, tmc_year, tmc_month, '6ee9263b4d5b8b76adb291bfb6ba03f1563a9d14')
        res = requests.get(url)
        res = get_json_from_TMC_response(res)
        return Response(res)
