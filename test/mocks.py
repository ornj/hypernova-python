import six
try:
    import httplib
except ImportError:
    import http.client as httplib

import json


class MockResponse(object):
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code or httplib.OK

    @property
    def ok(self):
        return httplib.OK <= self.status_code <= httplib.MULTIPLE_CHOICES

    def json(self):
        return self.json_data


def make_response_ok(*args, **kwargs):
    data = kwargs.get('json', {})
    results = {}
    for k, v in six.iteritems(data):
        results[k] = {
            'error': None, 
            'html': '<p>{}</p>'.format(json.dumps(v.get('data')))
        }
        
    return MockResponse({'error': None, 'results': results}, httplib.OK)


def make_response_component_error(*args, **kwargs):
    data = kwargs.get('json', {})
    results = {}
    for k, v in six.iteritems(data):
        results[k] = {
            'error': 'Something happened', 
            'html': '<p>{}</p>'.format(json.dumps(v.get('data')))
        }
    return MockResponse({'error': None, 'results': results}, httplib.OK)


def make_response_server_error(*args, **kwargs):
    return MockResponse(
        {'error': 'Kaboom', 'results': {}}, 
        httplib.INTERNAL_SERVER_ERROR
    )


def make_server_timeout(*args, **kwargs):
    return MockResponse({}, httplib.GATEWAY_TIMEOUT)