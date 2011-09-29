'''
Common enums

@author: jacekf
'''

class Http:
    """Enumerates HTTP methods"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

class HttpHeader:
    """Enumerates common HTTP headers"""
    CONTENT_TYPE = "content-type"
    ACCEPT = "accept"

class MediaType:
    """Enumerates media types"""    
    WILDCARD = "*/*"
    APPLICATION_XML = "application/xml"
    APPLICATION_ATOM_XML = "application/atom+xml"
    APPLICATION_XHTML_XML = "application/xhtml+xml"
    APPLICATION_SVG_XML = "application/svg+xml"
    APPLICATION_JSON = "application/json"
    APPLICATION_FORM_URLENCODED = "application/x-www-form-urlencoded"
    MULTIPART_FORM_DATA = "multipart/form-data"
    APPLICATION_OCTET_STREAM = "application/octet-stream"
    TEXT_PLAIN = "text/plain"
    TEXT_XML = "text/xml"
    TEXT_HTML = "text/html"
    TEXT_YAML = "text/yaml"