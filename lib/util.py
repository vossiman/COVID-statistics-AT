from urllib.request import urlopen, urlretrieve
from urllib.parse import urlparse
from cgi import parse_header
from pathlib import Path
import numpy as np

def retrieveDataFile(url, directory, prefix='data/'):
    """Downloads files into the data directory
    
    The downloaded file is saved in the `prefix` directory, organized by `directory` folders.
    
    This version honours the file name as advertised by the server. If the server does not
    advertise the filename in the HTTP headers, then it is derived from the URL.
    
    If a `prefix` is used, a trailing slash is expected.
    """
    remotefile = urlopen(url)
    content_disposition = remotefile.info()['Content-Disposition']
    filename = None
    if content_disposition is not None:
        value, params = parse_header(content_disposition)
        if params is not None:
            filename = params["filename"]
    if filename is None:
        filename = urlparse(url).path.split('/')[-1]
    path = prefix + directory
    Path(path).mkdir(parents=True, exist_ok=True)
    urlretrieve(url, path + '/' + filename)

    

def reds():
    """A generator for red colors, as consumed by matplotlib
    
    This generator yields five consecutively more faint reds, then repeats
    from bright red again.
    
    That's likely an overkill :-) but we could plot 6, 7 post-COVID years.
    """
    for n in np.linspace(0, 1, 5, False):
        yield (1, n  , n  , 1)
    yield from colors()