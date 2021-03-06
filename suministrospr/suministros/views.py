import os

from django.db.models import Count, Prefetch, Q
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from reversion.views import RevisionMixin

from ..utils.mixins import CacheMixin
from .constants import MUNICIPALITIES
from .forms import FilterForm, SuministroModelForm
from .models import Municipality, Suministro


class SuministroList(CacheMixin, TemplateView):
    cache_key = "suministro-list"
    template_name = "suministros/suministro_list.html"

    def get_context_data(self):
        data = super().get_context_data()
        suministros = Suministro.objects.defer("content").order_by("title")

        municipalities_with_suministros = (
            Municipality.objects.all()
            .prefetch_related(Prefetch("suministros", queryset=suministros,))
            .annotate(suministro_count=Count("suministro"))
            .filter(suministro_count__gt=0)
            .order_by("-suministro_count")
        )

        data["sorted_results"] = [
            {
                "count": municipality.suministro_count,
                "municipality": municipality.name,
                "suministros": municipality.suministros.all(),
            }
            for municipality in municipalities_with_suministros
        ]

        data["filter_form"] = FilterForm()

        return data


class SuministroByMunicipalityList(CacheMixin, ListView):
    model = Suministro
    template_name = "suministros/suministro_municipio_list.html"
    cache_key = "suministro-municipio-list"

    def get_cache_key(self):
        return f"{self.cache_key}:{self.kwargs['municipality']}"

    def get_queryset(self):
        return (
            Suministro.objects.select_related("municipality")
            .filter(municipality__slug=self.kwargs["municipality"])
            .defer("content")
            .order_by("title")
        )

    def get_context_data(self):
        data = super().get_context_data()
        data["municipality"] = MUNICIPALITIES.get(self.kwargs["municipality"])
        return data


class SuministroDetail(CacheMixin, DetailView):
    model = Suministro
    cache_key = "suministro-detail"
    queryset = (
        Suministro.objects.select_related("municipality").prefetch_related("tags").all()
    )

    def get_cache_key(self):
        return f"{self.cache_key}:{self.kwargs['slug']}"


class SuministroCreate(RevisionMixin, CreateView):
    model = Suministro
    form_class = SuministroModelForm

    def get_success_url(self):
        return reverse("suministro-detail", args=[self.object.slug])


class SuministroUpdate(RevisionMixin, UpdateView):
    model = Suministro
    form_class = SuministroModelForm

    def get_success_url(self):
        return reverse("suministro-detail", args=[self.object.slug])


class SuministroSearch(CacheMixin, TemplateView):
    template_name = "suministros/search.html"
    cache_key = "suministro-search"

    def get_cache_key(self):
        cache_key = self.cache_key
        tag = self.request.GET.get("tag")

        if tag:
            cache_key = f"{cache_key}:{tag}"

        return cache_key

    def get_context_data(self):
        data = super().get_context_data()
        data["results_total"] = 0
        data["results_municipalities"] = 0
        data["results"] = []

        filter_form = FilterForm(self.request.GET)

        suministros = Suministro.objects.all().defer("content").order_by("title")

        municipalities_with_suministros = (
            Municipality.objects.all()
            .prefetch_related(Prefetch("suministros", queryset=suministros))
            .annotate(suministro_count=Count("suministro",))
            .filter(suministro_count__gt=0)
            .order_by("-suministro_count")
        )

        if filter_form.is_valid():
            tag_slug = filter_form.cleaned_data["tag"]
            suministros = suministros.filter(tags__slug=tag_slug)

            municipalities_with_suministros = (
                Municipality.objects.all()
                .prefetch_related(Prefetch("suministros", queryset=suministros))
                .annotate(
                    suministro_count=Count(
                        "suministro",
                        filter=Q(suministro__tags__slug=tag_slug),
                        distinct=True,
                    )
                )
                .filter(suministro_count__gt=0, suministro__tags__slug=tag_slug)
                .order_by("-suministro_count")
            )

        for municipality in municipalities_with_suministros:
            data["results_total"] += municipality.suministro_count
            data["results_municipalities"] += 1
            data["results"].append(
                {
                    "count": municipality.suministro_count,
                    "municipality": municipality.name,
                    "suministros": municipality.suministros.all(),
                }
            )

        data["filter_form"] = filter_form

        return data


class SuministroServiceWorker(TemplateView):
    template_name = "common/service-worker.js"
    content_type = "application/javascript"

    def get_context_data(self):
        data = super().get_context_data()
        data["app_version"] = os.getenv("HEROKU_RELEASE_VERSION", "0.1.0")
        return data
