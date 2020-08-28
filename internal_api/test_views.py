import requests
import internal_api.views
import webapp.models

def test_should_return_tmc():
    credit_instance = webapp.models.Credit
    credit_instance.monto_uf = 500
    credit_instance.payment_deadline_days = 5
    credit_instance.payment_day_with_calculated_tmc = 6

    response = internal_api.views.CalculateTMCForCredit.post(None, None, credit_instance)
    assert response.status_code == 200
    
def test_conversion_should_return_float_type():
    value = '28.666,50'
    current = internal_api.views.replace_chilean_decimals(value)
    assert type(current) is float

def test_conversion_should_return_valid_float():
    value = '28.666,50'
    expected = 28666.5
    current = internal_api.views.replace_chilean_decimals(value)
    assert current == expected


class ResponseDataMock():
    data = int

ResponseDataMock.data = {
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

def test_should_return_value_for_type_26():
    current = internal_api.views.get_type_of_tmc(2000, ResponseDataMock)
    expected = "35.04"
    assert current == expected

def test_should_return_value_for_type_25():
    current = internal_api.views.get_type_of_tmc(6000, ResponseDataMock)
    expected = "6.81"
    assert current == expected
