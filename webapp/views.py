import re
from datetime import datetime
from django.shortcuts import render


def home(request):
    return render(request, "webapp/home.html")
    # return render(
    #     request,
    #     'webapp/home.html',
    #     {
    #         'name': 'Luis',
    #         'date': datetime.now()
    #     }
    # )
