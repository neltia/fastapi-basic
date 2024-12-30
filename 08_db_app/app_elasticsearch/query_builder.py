from elasticsearch_dsl import Search, Q


class QueryBuilder:
    @staticmethod
    def build_search_query(query: str = None, filters: dict = None, sort_by: str = None, order: str = "asc"):
        """
        상품 검색 쿼리 생성
        :param query: 검색어
        :param filters: 필터 조건
        :param sort_by: 정렬 기준
        :param order: 정렬 방향
        :return: Elasticsearch Query DSL
        """
        search = Search()

        # 검색어 추가
        if query:
            search = search.query(Q("match", name=query))

        # 필터 추가
        if filters:
            for field, value in filters.items():
                search = search.filter(Q("term", **{field: value}))

        # 정렬 추가
        if sort_by:
            search = search.sort({sort_by: {"order": order}})

        return search
