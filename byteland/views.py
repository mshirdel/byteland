from datetime import datetime
from django.shortcuts import render


def index(request):
    return render(request, 'byteland/index.html',
                  {'msg': str(request.META['REMOTE_ADDR']), 'dt': datetime.now()})
