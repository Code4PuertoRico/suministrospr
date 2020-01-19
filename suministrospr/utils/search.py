from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from ..suministros.models import Suministro

suministros_search_vector = (
    SearchVector("title", weight="B")
    + SearchVector("content", weight="A")
    + SearchVector("municipality__name", weight="C")
    + SearchVector("tags__name", weight="C")
)

municipality_search_vector = SearchVector("name")
tags_search_vector = SearchVector("name")


def search(query):
    keyword_search_query = SearchQuery(query)
    phrase_search_query = SearchQuery(query, search_type="phrase")
    final_search_query = keyword_search_query | phrase_search_query
    search_rank = SearchRank(suministros_search_vector, final_search_query)

    suministros = Suministro.objects.annotate(rank=search_rank).order_by("-rank")

    return suministros
