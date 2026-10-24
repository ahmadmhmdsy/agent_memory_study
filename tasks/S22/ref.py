from urllib.parse import urlsplit, parse_qsl


def scheme(url):
    return url.split("://", 1)[0].lower()


def host(url):
    return urlsplit(url).hostname


def path(url):
    return urlsplit(url).path or "/"


def query_params(url):
    return dict(parse_qsl(urlsplit(url).query))


def is_secure(url):
    return scheme(url) == "https"
