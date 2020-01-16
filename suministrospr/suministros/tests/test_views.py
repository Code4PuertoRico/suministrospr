import pytest
from django.urls import reverse

from ..models import Suministro
from ..views import SuministroList


@pytest.mark.django_db
class TestSuministroList:
    url = reverse("suministro-list")

    def test_get_returns_200(self, rf):
        request = rf.get(self.url)
        response = SuministroList.as_view()(request)
        assert response.status_code == 200

    def test_order_by_count(self, rf):
        Suministro.objects.bulk_create(
            [
                Suministro(
                    title="test A",
                    slug="test-a",
                    municipality="guanica",
                    content="test a",
                ),
                Suministro(
                    title="test B",
                    slug="test-b",
                    municipality="guayanilla",
                    content="test b",
                ),
                Suministro(
                    title="test C",
                    slug="test-c",
                    municipality="ponce",
                    content="test c",
                ),
                Suministro(
                    title="test D",
                    slug="test-d",
                    municipality="guayanilla",
                    content="test d",
                ),
                Suministro(
                    title="test E",
                    slug="test-e",
                    municipality="guanica",
                    content="test e",
                ),
                Suministro(
                    title="test F",
                    slug="test-F",
                    municipality="guanica",
                    content="test f",
                ),
            ]
        )
        request = rf.get(self.url)
        response = SuministroList.as_view()(request)

        results = response.context_data["sorted_results"]

        assert results[0]["municipality"] == "Guánica"
        assert results[0]["count"] == 3

        assert results[1]["municipality"] == "Guayanilla"
        assert results[1]["count"] == 2

        assert results[2]["municipality"] == "Ponce"
        assert results[2]["count"] == 1
