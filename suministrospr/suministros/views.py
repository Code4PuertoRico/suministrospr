from django.views.generic.edit import CreateView, UpdateView

from .models import Suministro


class SuministroCreate(CreateView):
    model = Suministro
    fields = ["title", "municipality", "content"]


class SuministroUpdate(UpdateView):
    model = Suministro
    fields = ["title", "municipality", "content"]
