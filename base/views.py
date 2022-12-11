from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
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

class RoomsView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    template_name = 'base/rooms.html'
    model = Room
    permission_required = 'base.view_room'


@login_required  # jen pro view typu funkce a ne pro třídu
@permission_required(['base.view_room', 'base.view_message'])
def room(request, pk):
    LOGGER.warning(request.method)
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        if request.user.has_perms('base.add_message'):
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


class RoomCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'base/room_form.html'
    extra_context = {'title': 'CREATE !!!'}
    form_class = RoomForm
    success_url = reverse_lazy('rooms')
    permission_required = 'base.add_room'

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


class RoomUpdateView( PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'base/room_form.html'
    extra_context = {'title': 'UPDATE !!!'}
    form_class = RoomForm
    success_url = reverse_lazy('rooms')
    model = Room
    permission_required = 'base.change_room'

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class RoomDeleteView(StaffRequiredMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'base/room_confirm_delete.html'
    model = Room
    success_url = reverse_lazy('rooms')
    permission_required = 'base.delete_room'

def handler403(request, exception):
   return render(request, '403.html', status=403)
