# from django.db.models import Q
# # from .models import ApiKey
# from rest_framework.permissions import BasePermission
# from hashlib import md5
# from .utils import sort_query_string
# from django.utils import timezone
# from datetime import datetime
#
#
# def restore_request_sign(url, api_secret):
#     """Retrieve Sign from url and api_secret"""
#     # print('received request: ', url)
#     query_string = url.split('?')[1] if '?' in url else url
#     data_string = query_string.split('&sign')[0]
#     # print('deleted sign: ', data_string)
#     data = sort_query_string(data_string) + 'api_secret=' + api_secret
#     # print('data to encode: ', data)
#     sign = md5(data.encode('utf-8')).hexdigest()
#     # print('should have a sign: ', sign)
#     return sign
#
#
# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip
#
#
# def has_source_ip_permission(APP_KEY_SECRETS, api_key, source_ip=''):
#     app_key_secret = next((x for x in APP_KEY_SECRETS if x['api_key'] == api_key), None)
#     message = 'OK'
#     if not app_key_secret:
#         message = 'KEY Not Found'
#         return False, message
#     elif not app_key_secret['source']:
#         message = 'OK, no Source control provided, all Source IPs are allowed'
#         return True, message
#     else:
#         api_source = app_key_secret['source']
#         ip_list = api_source.replace(' ', '').split(',')
#         if source_ip.split('.')[0] in ip_list:
#             return True, message
#         else:
#             message = 'Source IP not allowed'
#             return False, message
#
#
# def has_permission(APP_KEY_SECRETS, api_key, source_ip=''):
#     message = "api sign incorrect."
#     app_keys = app_key_secret = next((x for x in APP_KEY_SECRETS if x['api_key'] == api_key), None)
#     timestamp = app_keys['timestamp']
#     sign = app_keys['sign']
#     try:
#         key = app_keys['api_key']
#         api_secret = app_keys['api_secret']
#         api_timeout_in = app_keys['timeout_in']
#         api_expired_at = app_keys['expired_at']
#     except ApiKey.DoesNotExist:
#         self.message = "api key not found."
#         return False
#
#     # Check timeout
#     if has_timeout(timestamp, api_timeout_in):
#         self.message = "api request timeout, please create new timestamp for new request."
#         return False
#
#     # Check key expired
#     if has_expired(api_expired_at):
#         self.message = "API Key and Secret has expired."
#         return False
#
#     # print('query_string: ', query_string)
#     restored_sign = restore_request_sign(query_string, api_secret)
#     # print('restored sign: ', restored_sign)
#     # print('if correct: ', restored_sign == sign)
#     # print('Should have a sign', sign)
#     # print(api_secret, api_timeout_in)
#     return restored_sign == sign
#
#
# class CheckApiKeyAuth(BasePermission):
#     def has_permission(self, request, view):
#         api_key = request.query_params.get('api_key')
#         post_secret = request.query_params.get('api_secret')
#         try:
#             obj = ApiKey.objects.get(Q(api_key=api_key, revoked=False),
#                                      Q(expired_at__isnull=True) |
#                                      Q(expired_at__gt=timezone.now()))
#             api_secret = obj.api_secret
#         except ApiKey.DoesNotExist:
#             return False
#
#         return post_secret == api_secret
#
#
# def has_timeout(timestamp, timeout_in):
#     if timeout_in <= 0:
#         return False
#     timestamp_object = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
#     now = timezone.now().today()
#     now_unix = round(now.timestamp())
#     timestamp_unix = round(timestamp_object.timestamp())
#     interval = now_unix - timestamp_unix
#     # print('now', now.strftime('%Y%m%d%H%M%S'), 'dest:', timestamp_object)
#     # print('now', now_unix, 'dest:', timestamp_unix)
#     # print(interval, timeout_in)
#     return interval > timeout_in
#
#
# def has_expired(expired_at):
#     if expired_at and isinstance(expired_at, datetime):
#         now = timezone.now()
#         return now > expired_at
#     else:
#         return False
