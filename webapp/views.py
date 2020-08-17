import re
import json
from datetime import datetime
from django.shortcuts import render
from webapp.forms import CreditForm
from webapp.models import Credit
from cumplo_api.views import CalculateTMCForCredit


def home(request):
    return render(request, "webapp/home.html")

def credit(request):
    form = CreditForm(request.POST or None)
    credit_instance = Credit()

    if request.method == "POST":
        if form.is_valid():
            message = "Los días de plazo no pueden ser mayores al cálculo de la tmc, intente nuevamente"
            credit_instance.monto_uf = form.cleaned_data['monto_uf']
            credit_instance.payment_deadline_days = form.cleaned_data['payment_deadline_days']
            credit_instance.payment_day_with_calculated_tmc = form.cleaned_data['payment_day_with_calculated_tmc']

            # días de plazo no pueden ser mayores al cálculo de la tmc
            if credit_instance.payment_deadline_days > credit_instance.payment_day_with_calculated_tmc:
                return render(request, "webapp/credit.html", {"form": form, "message": message})
            elif credit_instance.payment_deadline_days > 90:
                message = "El plazo máximo es de 90 días"
                return render(request, "webapp/credit.html", {"form": form, "message": message})
            else:
                view = CalculateTMCForCredit.post(request, credit_instance, None)
                #calculate_res = view(request, credit_instance)
                new_value = json.loads(view.data)
                
                return render(request, "webapp/rate_tmc.html", {"uf": new_value['credito']} )
        render(request, "webapp/credit.html")
    else:
        return render(request, "webapp/credit.html", {"form": form})
