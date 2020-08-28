import requests
from django.conf import settings
import external_api.views

def test_should_return_today_uf_status_200():
    response = external_api.views.TodayUF.get(None, None)
    assert response.status_code == 200

def test_should_return_today_uf_as_float():
    response = external_api.views.TodayUF.get(None, None)
    uf = response.data['UFs'][0]["Valor"]
    uf = uf.replace('.', '').replace(',', '.')
    uf_value = float(uf)
    assert type(uf_value) is float

def test_valid_dict_in_case_of_error_response_from_today_uf():
    today_uf_dict = external_api.views.get_json_from_UF_response('not_valid')
    assert type(today_uf_dict) is dict

def test_should_return_tmc():
    kwargs = { 
        'year': 2020, 
        'month': 8 
    }
    response = external_api.views.TMCByYearAndMonth.get(None, None, kwargs=kwargs)
    assert response.status_code == 200

def test_valid_dict_in_case_of_error_response_from_tmc():
    tmc_dict = external_api.views.get_json_from_TMC_response('not_valid')
    assert type(tmc_dict) is dict
