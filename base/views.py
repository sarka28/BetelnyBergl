from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, CreateView, UpdateView, DeleteView

from base.forms import RoomForm, LOGGER
from base.models import Room, Message


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

@login_required #jen pro view typu funkce a ne pro třídu
def room(request, pk):
    LOGGER.warning(request.method)
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        room.save()
        return redirect('room', pk=pk)

    messages = room.message_set.all()
    context = {'messages': messages, 'room': room}
    return render(request, template_name='base/room.html', context=context)


class RoomCreateView(LoginRequiredMixin, CreateView):
    template_name = 'base/room_form.html'
    extra_context = {'title': 'CREATE !!!'}
    form_class = RoomForm
    success_url = reverse_lazy('rooms')

    def form_valid(self, form):
        result = super().form_valid(form)
        LOGGER.warning(form.cleaned_data)
        return result

    # def form_valid(self, form):
    #     cleaned_data = form.cleaned_data
    #     Room.objects.create(
    #         name=cleaned_data['name'],
    #         description=cleaned_data['description']
    #     )
    #     return super().form_valid(form)

class RoomUpdateView(UpdateView):
    template_name = 'base/room_form.html'
    extra_context = {'title': 'UPDATE !!!'}
    form_class = RoomForm
    success_url = reverse_lazy('rooms')
    model = Room

class RoomDeleteView(DeleteView):
    template_name = 'base/room_confirm_delete.html'
    model = Room
    success_url = reverse_lazy('rooms')


