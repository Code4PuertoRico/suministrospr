from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Suministro
from .forms import SuministroModelForm


class SuministroList(ListView):
    model = Suministro


class SuministroDetail(DetailView):
    model = Suministro


class SuministroCreate(CreateView):
    model = Suministro
    form_class = SuministroModelForm

    def get_success_url(self):
        return reverse("suministro-edit", args=[self.object.slug])


class SuministroUpdate(UpdateView):
    model = Suministro
    form_class = SuministroModelForm

    def get_success_url(self):
        return reverse("suministro-detail", args=[self.object.slug])
