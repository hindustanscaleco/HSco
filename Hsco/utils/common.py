from django.core.paginator import Paginator


def paginate_data(queryset, page_number, items_per_page=30):
    """
    Paginates a queryset and returns the data for the specified page number.

    Args:
    - queryset: The queryset containing the data to paginate.
    - page_number: The number of the page to retrieve.
    - items_per_page: The number of items to display per page (default is 10).

    Returns:
    - A dictionary containing the paginated data and pagination information.
    """
    paginator = Paginator(queryset, items_per_page)
    page_obj = paginator.get_page(page_number)
    return {
        'page_obj': page_obj,
        'paginator': paginator,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
    }
