from django.urls import path

from .views import SuministroCreate, SuministroDetail, SuministroUpdate, SuministroList

urlpatterns = [
    path("", SuministroList.as_view(), name="suministro-list"),
    path("suministros/add/", SuministroCreate.as_view(), name="suministro-add"),
    path(
        "suministros/<slug:slug>/", SuministroDetail.as_view(), name="suministro-detail"
    ),
    path(
        "suministros/<slug:slug>/edit",
        SuministroUpdate.as_view(),
        name="suministro-edit",
    ),
]
