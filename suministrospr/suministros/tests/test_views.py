import pytest
from django.urls import reverse

from ..views import SuministroList


@pytest.mark.django_db
class TestSuministroList:
    url = reverse("suministro-list")

    def test_get_returns_200(self, rf):
        request = rf.get(self.url)
        response = SuministroList.as_view()(request)
        assert response.status_code == 200
