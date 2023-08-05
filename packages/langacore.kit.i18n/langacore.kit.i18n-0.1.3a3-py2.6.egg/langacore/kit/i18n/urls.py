# based on http://stackoverflow.com/questions/804336/

import urlparse, urllib

def uni2ascii(url, convert_whitespace=True, to_lower=True):
    if not isinstance(url, unicode):
        # turn string into unicode
        url = url.decode('utf8')

    if to_lower:
        url = url.lower()

    if convert_whitespace:
        url = url.replace(u' ', u'_').replace(u'\t', u'_').replace(u'\n', u'').replace(u'\r', u'')

    # parse it
    parsed = urlparse.urlsplit(url)

    # encode each component
    scheme = parsed.scheme.encode('utf8')
    netloc = parsed.netloc.encode('idna')
    path = '/'.join(  # could be encoded slashes!
        urllib.quote(urllib.unquote(pce).encode('utf8'),'')
        for pce in parsed.path.split('/')
    )
    query = urllib.quote(urllib.unquote(parsed.query).encode('utf8'),'=&?/')
    fragment = urllib.quote(urllib.unquote(parsed.query).encode('utf8'))

    # put it back together
    result = urlparse.urlunsplit((scheme,netloc,path,query,fragment))

    return result
