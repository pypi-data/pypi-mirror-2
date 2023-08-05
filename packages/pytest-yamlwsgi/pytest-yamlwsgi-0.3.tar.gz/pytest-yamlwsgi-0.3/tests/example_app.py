

def simple_app(environ, start_response):
    path = environ['PATH_INFO']

    if path == '/':
        status = '200 OK'
        response_headers = [('Content-type','text/plain')]
        start_response(status, response_headers)
        return ['Hello world!\n']

    elif path == '/err':
        status = '404 OK'
        response_headers = [('Content-type','text/html')]
        start_response(status, response_headers)
        return ['Not Found\n']

    elif path == '/new':
        status = '200 OK'
        response_headers = [('Content-type','text/html')]
        start_response(status, response_headers)
        return ['New\n']

    else:
        status = '404 OK'
        response_headers = [('Content-type','text/html')]
        start_response(status, response_headers)
        return ['Not Found\n']


def app_factory():
    return simple_app

