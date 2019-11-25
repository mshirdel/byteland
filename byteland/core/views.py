from datetime import datetime
from django.shortcuts import render


def sudo_view(request, *args, **kwargs):
    return render(request, 'byteland/not_implemented.html')
