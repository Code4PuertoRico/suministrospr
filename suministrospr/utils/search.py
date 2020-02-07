from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

suministros_search_vector = (
    SearchVector("title", weight="B")
    + SearchVector("content", weight="A")
    + SearchVector("municipality__name", weight="C")
    + SearchVector("tags__name", weight="C")
)

municipality_search_vector = SearchVector("name")
tags_search_vector = SearchVector("name")


def search(query, tag_slug, suministros):
    if tag_slug:
        suministros = suministros.filter(tags__slug=tag_slug)

    if query:
        keyword_search_query = SearchQuery(query)
        phrase_search_query = SearchQuery(query, search_type="phrase")
        final_search_query = keyword_search_query | phrase_search_query
        search_rank = SearchRank(suministros_search_vector, final_search_query)

        suministros = (
            suministros.annotate(search=suministros_search_vector, rank=search_rank)
            .filter(search=final_search_query)
            .order_by("-rank")
        )

    return suministros.distinct()
