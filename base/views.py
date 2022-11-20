from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from base.models import Room


def hello(request):
    s = request.GET.get('s', '')
    return HttpResponse(f"Ahoj {s}!!!")

def rooms(request):
    rooms =Room.objects.all()
    context = {'rooms': rooms}
    return render(request, template_name='base/rooms.html',context=context)
