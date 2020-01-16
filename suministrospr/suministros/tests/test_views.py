import pytest
from django.urls import reverse

from ..models import Municipality, Suministro
from ..views import SuministroList


@pytest.mark.django_db
class TestSuministroList:
    url = reverse("suministro-list")

    def test_get_returns_200(self, rf):
        request = rf.get(self.url)
        response = SuministroList.as_view()(request)
        assert response.status_code == 200

    def test_order_by_count(self, rf, django_assert_num_queries):

        guayanilla = Municipality.objects.create(name="Guayanilla")
        ponce = Municipality.objects.create(name="Ponce")
        guanica = Municipality.objects.create(name="Guánica")

        Suministro.objects.bulk_create(
            [
                Suministro(title="test A", municipality=guanica, content="test a",),
                Suministro(title="test B", municipality=guayanilla, content="test b",),
                Suministro(title="test C", municipality=ponce, content="test c",),
                Suministro(title="test D", municipality=guayanilla, content="test d",),
                Suministro(title="test E", municipality=guanica, content="test e",),
                Suministro(title="test F", municipality=guanica, content="test f",),
            ]
        )

        with django_assert_num_queries(2):
            request = rf.get(self.url)
            response = SuministroList.as_view()(request)

        results = response.context_data["sorted_results"]

        assert results[0]["municipality"] == "Guánica"
        assert results[0]["count"] == 3

        assert results[1]["municipality"] == "Guayanilla"
        assert results[1]["count"] == 2

        assert results[2]["municipality"] == "Ponce"
        assert results[2]["count"] == 1
