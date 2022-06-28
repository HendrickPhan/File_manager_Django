from django.conf import settings

class CacheHeaderMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path.split("/")[1:3]
        if ((path[0] == 'file' or path[0] == 'media') 
            and path[1] == 'images'
            and (response.status_code == 200 or response.status_code == 302)):
            response['Cache-Control'] = "public, max-age=%s" % (settings.FILE_CACHE_TIME, )

        return response