import pytest
from django.urls import reverse

from ..models import Municipality, Suministro, Tag
from ..views import SuministroList, SuministroSearch


@pytest.mark.django_db
class TestSuministroList:
    url = reverse("suministro-list")

    @pytest.fixture(autouse=True)
    def setup_fixture(self):
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

    def test_get_returns_200(self, rf):
        request = rf.get(self.url)
        response = SuministroList.as_view()(request)
        assert response.status_code == 200

    def test_order_by_count(self, rf, django_assert_num_queries):
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


@pytest.mark.django_db
class TestSuministroSearch:
    url = reverse("suministro-search")

    @pytest.fixture(autouse=True)
    def setup_fixture(self):
        guayanilla = Municipality.objects.create(name="Guayanilla")
        ponce = Municipality.objects.create(name="Ponce")
        guanica = Municipality.objects.create(name="Guánica")

        tag_a = Tag.objects.create(name="tag_a")
        tag_b = Tag.objects.create(name="tag_b")

        suministro_a = Suministro.objects.create(
            title="test A", municipality=guanica, content="test a"
        )
        suministro_a.tags.add(tag_a, tag_b)

        suministro_b = Suministro.objects.create(
            title="test B", municipality=guayanilla, content="test b"
        )
        suministro_b.tags.add(tag_a)

        suministro_c = Suministro.objects.create(
            title="test C", municipality=ponce, content="test c"
        )
        suministro_c.tags.add(tag_b)

    def test_get_returns_200(self, rf):
        request = rf.get(self.url)
        response = SuministroSearch.as_view()(request)
        assert response.status_code == 200

    def test_results_total_without_filter(self, rf):
        request = rf.get(self.url)
        response = SuministroSearch.as_view()(request)
        results_total = response.context_data["results_total"]
        assert results_total == 3

    def test_results_total_with_filter(self, rf):
        request = rf.get(self.url, {"tag": "tag_a"})
        response = SuministroSearch.as_view()(request)
        results_total = response.context_data["results_total"]
        assert results_total == 2

    def test_results_municipalities_without_filter(self, rf):
        request = rf.get(self.url)
        response = SuministroSearch.as_view()(request)
        results_municipalities = response.context_data["results_municipalities"]
        assert results_municipalities == 3

    def test_results_municipalities_with_filter(self, rf):
        request = rf.get(self.url, {"tag": "tag_a"})
        response = SuministroSearch.as_view()(request)
        results_municipalities = response.context_data["results_municipalities"]
        assert results_municipalities == 2

    def test_num_queries_without_filter(self, rf, django_assert_num_queries):
        with django_assert_num_queries(4):
            request = rf.get(self.url)
            response = SuministroSearch.as_view()(request)
            assert response.rendered_content

    def test_num_queries_with_filter(self, rf, django_assert_num_queries):
        with django_assert_num_queries(5):
            request = rf.get(self.url, {"tag": "tag_a"})
            response = SuministroSearch.as_view()(request)
            assert response.rendered_content
