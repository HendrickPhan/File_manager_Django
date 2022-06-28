from django.http import JsonResponse

def json_response_success(data, message = ''):
    response = {
        'code': 200,
        'data': data,
        'success': True,
        'msg': message
    }
    return JsonResponse(response)

def json_response_failure(message, code=400):
    response = {
        'code': code,
        'success': False,
        'msg': message
    }
    return JsonResponse(response)