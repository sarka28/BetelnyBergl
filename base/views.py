from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, CreateView

from base.forms import RoomForm
from base.models import Room


def hello(request):
    s = request.GET.get('s', '')
    return HttpResponse(f"Ahoj {s}!!!")


# def rooms(request):
#    rooms = Room.objects.all()
#     context = {'rooms': rooms}
#    return render(request, template_name='base/rooms.html', context=context)

class RoomsView(ListView):
    template_name = 'base/rooms.html'
    model = Room


def room(request, id):
    room = Room.objects.get(id=id)
    messages = room.message_set.all()
    context = {'messages': messages, 'room': room}
    return render(request, template_name='base/room.html', context=context)


class RoomCreateView(CreateView):
    template_name = 'base/room_form.html'
    form_class = RoomForm
    success_url = reverse_lazy('rooms')

    # def form_valid(self, form):
    #     cleaned_data = form.cleaned_data
    #     Room.objects.create(
    #         name=cleaned_data['name'],
    #         description=cleaned_data['description']
    #     )
    #     return super().form_valid(form)
