from django.urls import path

from .views import SuministroCreate, SuministroUpdate

urlpatterns = [
    path('suministros/add/', SuministroCreate.as_view(), name='suministro-add'),
    path('suministros/<int:pk>/', SuministroUpdate.as_view(), name='suministro-update'),
]
