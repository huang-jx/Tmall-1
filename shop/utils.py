import json

from django.http import HttpResponse


def response_json(data=None, status=200, msg='success'):
    result = {}
    if data:
        result.update(data=data)
    result.update(status=status, msg=msg)
    return HttpResponse(json.dumps(result), content_type='application/json')
