from django import forms
from django.core.paginator import Paginator

from team_finder.constants import GITHUB_URL_PATTERN, PROJECTS_PER_PAGE


def paginate(queryset, request, per_page=PROJECTS_PER_PAGE):
    page_number = request.GET.get('page', 1)
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)


def validate_github_url(url):
    if url and GITHUB_URL_PATTERN not in url:
        raise forms.ValidationError('Ссылка должна вести на github.com')
    return url  