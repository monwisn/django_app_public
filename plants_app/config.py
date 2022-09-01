from django.core.paginator import Paginator


def pagination(request, data, num=15):
    paginator = Paginator(data, num)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj
