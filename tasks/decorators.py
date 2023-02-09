from django.http import HttpRequest, HttpResponse


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def source_ip_control(func):
    """
    Check source IP addr
    """
    ip_list = ['127', '192', '172', '10']

    def _view(request, *args, **kwargs):
        ip = get_client_ip(request)
        is_allowed = ip.split('.')[0] in ip_list
        if is_allowed:
            return func(request, *args, **kwargs)
        else:
            return HttpResponse('source {} not allowed'.format(ip))

    return _view
