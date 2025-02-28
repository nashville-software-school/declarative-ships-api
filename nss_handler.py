import json
from enum import Enum
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler


class status(Enum):
    SUCCESS = 200
    CREATED = 201
    SUCCESS_NO_BODY = 204
    BAD_REQUEST = 400
    NOT_FOUND = 404
    UNSUPPORTED_METHOD = 405
    SERVER_ERROR = 500

class HandleRequests(BaseHTTPRequestHandler):

    def response(self, body, code):
        """Send HTTP response with body and status code

        Args:
            body (any): Data to send in response
            code (int): HTTP response code
        """
        self.set_response_code(code)
        self.wfile.write(body.encode())

    def get_request_body(self):
        """Extract body from HTTP request

        Returns:
            string: JSON serialized request body
        """
        content_len = int(self.headers.get('content-length', 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)
        return request_body

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')
        resource = path_params[1]

        url_dictionary = {
            "requested_resource": resource,
            "query_params": {},
            "pk": 0
        }

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            url_dictionary["query_params"] = query

        try:
            pk = int(path_params[2])
            url_dictionary["pk"] = pk
        except (IndexError, ValueError):
            pass

        return url_dictionary

    def set_response_code(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()
