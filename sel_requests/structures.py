from requests.structures import CaseInsensitiveDict
from urllib.parse import urlencode
import json as _json

class Request:
    headers: CaseInsensitiveDict
    method: str
    url: str
    data: (str, bytes, dict)
    
    def __init__(self, method, url, data=None,
                 json=None, headers=None):
        self.headers = CaseInsensitiveDict(headers)
        self.method = method
        self.url = url

        if json is not None:
            self.headers["Content-Type"] = "application/json; charset=UTF-8"
            self.data = _json.dumps(json, separators=(",", ":"))
        
        elif type(data) == dict:
            self.headers["Content-Type"] = "application/x-www-form-urlencoded"
            self.data = urlencode(data)
        
        else:
            self.data = data
    
class Response:
    url: str
    ok: bool
    status_code: int
    reason: str
    text: str
    content: bytes
    headers: CaseInsensitiveDict

    def __init__(self, url, text, headers, status_code, reason, ok):
        self.url = url
        self.ok = ok
        self.status_code = status_code
        self.reason = reason
        self.text = text
        self.content = text.encode("UTF-8")
        self.headers = CaseInsensitiveDict(headers)

    def __repr__(self):
        return "<Response [%d]>" % self.status_code

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return

    def json(self):
        return _json.loads(self.text)