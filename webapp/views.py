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
                new_value = json.loads(view.data)
                total_delay_days = credit_instance.payment_day_with_calculated_tmc - credit_instance.payment_deadline_days
                total_value_with_tmc = f"{new_value['total_value'] + new_value['tmc']:,}"

                context = {
                    "total_value": f"{new_value['total_value']:,}",
                    "tmc": f"{new_value['tmc']:,}",
                    "message": "El total a pagar por %d día(s) de mora es de $ %s" % (total_delay_days, total_value_with_tmc)
                }
                return render(request, "webapp/rate_tmc.html", context)
        render(request, "webapp/credit.html")
    else:
        return render(request, "webapp/credit.html", {"form": form})
