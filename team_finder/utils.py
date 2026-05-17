from django.core.paginator import Paginator


def paginate(queryset, request, per_page=12):
    
    page_number = request.GET.get('page', 1)
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)