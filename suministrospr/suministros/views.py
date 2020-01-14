from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from .constants import MUNICIPALITIES
from .models import Suministro
from .forms import SuministroModelForm


class SuministroList(ListView):
    model = Suministro

    def get_queryset(self):
        return (
            Suministro.objects.all().defer("content").order_by("municipality", "title")
        )


class SuministroByMunicipalityList(ListView):
    model = Suministro
    template_name = "suministros/suministro_municipio_list.html"

    def get_queryset(self):
        return (
            Suministro.objects.filter(municipality=self.kwargs["municipality"])
            .defer("content")
            .order_by("municipality", "title")
        )

    def get_context_data(self):
        data = super().get_context_data()
        data["municipality"] = MUNICIPALITIES.get(self.kwargs["municipality"])
        return data


class SuministroDetail(DetailView):
    model = Suministro


class SuministroCreate(CreateView):
    model = Suministro
    form_class = SuministroModelForm

    def get_success_url(self):
        return reverse("suministro-detail", args=[self.object.slug])


class SuministroUpdate(UpdateView):
    model = Suministro
    form_class = SuministroModelForm

    def get_success_url(self):
        return reverse("suministro-detail", args=[self.object.slug])
