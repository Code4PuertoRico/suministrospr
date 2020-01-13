from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .models import Suministro


class SuministroCreate(CreateView):
    model = Suministro
    fields = ["title", "municipality", "content"]
    success_url = reverse_lazy('suministro-add')


class SuministroUpdate(UpdateView):
    model = Suministro
    fields = ["title", "municipality", "content"]
