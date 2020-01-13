from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Suministro


class SuministroList(ListView):
    model = Suministro


class SuministroDetail(DetailView):
    model = Suministro


class SuministroCreate(CreateView):
    model = Suministro
    fields = ["title", "municipality", "content"]

    def get_success_url(self):
        return reverse("suministro-edit", args=[self.object.id])


class SuministroUpdate(UpdateView):
    model = Suministro
    fields = ["title", "municipality", "content"]

    def get_success_url(self):
        return reverse("suministro-detail", args=[self.object.id])
