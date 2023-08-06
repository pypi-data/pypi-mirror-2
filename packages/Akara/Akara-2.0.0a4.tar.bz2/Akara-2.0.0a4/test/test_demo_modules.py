# This tests Akara through a running web server, started on an unused port.
# Some of the tests will require Akara to connect to other machines, which
# means this must be run with a working network.

# NOTE: you can test against a running server by setting AKARA_TEST_SERVER
# Here's one way to use a server on a different port on localhost:
#   env AKARA_TEST_SERVER=localhost:49658 nosetests test_demo_modules.py
# I do this to get around the server startup costs when developing/debugging tests.

from server_support import server

import urllib, urllib2
from urllib2 import urlopen
import os
from email.utils import formatdate

from amara import bindery
from amara.lib import iri
from amara.tools import atomtools

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "resource")

# the index "/"
def test_index():
    url = server()
    s = urlopen(url).read()
    assert "http://purl.org/xml3k/akara/services/registry" in s
    assert "akara.atom.json" in s

def test_index_search():
    url = server() + "?service=http://purl.org/xml3k/akara/services/registry"
    s = urlopen(url).read()
    assert "http://purl.org/xml3k/akara/services/registry" in s
    assert "akara.atom.json" not in s
    

# atomtools.py
def test_atom_json():
    from amara.thirdparty import json
    url = server() + "akara.atom.json?url=http://zepheira.com/feed/atom/"
    response = urlopen(url)
    results = json.load(response)
    items = results["items"]
    for item in items:
        assert "title" in item
test_atom_json.network=True

def test_aggregate_atom():
    url = server() + "akara.aggregate.atom"
    response = urlopen(url)
    doc = bindery.parse(response, model=atomtools.FEED_MODEL)
    assert str(doc.feed.title[0]) == "Feed me!", str(doc.feed.title[0])
    assert len(doc.feed.entry) == 3, len(doc.feed.entry)

def test_webfeedjson():
    from amara.thirdparty import json
    import json
    url = server() + "akara.webfeed.json?url=http://feeds.delicious.com/v2/rss/recent%3Fmin=1%26count=15"
    response = urlopen(url)
    results = json.load(response)
    print results

# calweb.py

# Frankly, this module doesn't seem that useful, so I'll only check
# to see that I get a response and that it contains a "akaraCalendarToday"
def test_calendar():
    url = server() + "akara.calendar"
    s = urlopen(url).read()
    assert "akaraCalCalendarToday" in s


# icaltools.py

def test_ical2json():
    from amara.thirdparty import json

    ical_filename = os.path.join(RESOURCE_DIR, "icalendar_test.ics")
    url = server() + "ical.json"

    req = urllib2.Request(url)
    req.add_header('Content-Type', 'text/calendar')

    data = open(ical_filename).read()

    response = urllib2.urlopen(req, data)
    results = json.load(response)

    items = results["items"]
    assert len(items) == 2
    assert items[0]["summary"] == "Bastille Day Party"
    assert items[1]["summary"] == "Akara test"

# luckygoogle.py

def test_luckygoogle():
    url = server() + "akara.luckygoogle?q=google"
    response = urlopen(url)
    s = response.read()
    assert s == "http://www.google.com/\n", repr(s)


# markuptools.py
def test_akara_twc():
    url = server() + "akara.twc.xml?max=5" # max 5 words in the result

    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/xml')

    data = "<a>one two <b>three four </b><c>five <d>six seven</d> eight</c> nine</a>"
    
    result = urllib2.urlopen(req, data).read()
    assert "one" in result, repr(result)
    assert "five" in result, repr(result)
    assert "six" not in result, repr(result)
    assert "nine" not in result, repr(result)

def test_akara_twc_html():
    url = server() + "akara.twc.xml?html=yes&max=11" # max 11 words

    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/xml')

    data = ("<html><head/><body>" + " ".join(map(str, range(510))) + "</body></html>")
    
    result = urllib2.urlopen(req, data).read()
    assert "7 8 9 10" in result, repr(result)
    assert "11" not in result, repr(result)

# method_dispatcher.py

def test_method_dispatcher_get():
    url = server() + "vikings?word=spam"
    response = urlopen(url)
    s = response.read()
    assert "spam-itty spam" in s, s

def test_method_dispatcher_get2():
    url = server() + "vikings?word=Spam"
    response = urlopen(url)
    s = response.read()
    assert "Spam-itty Spam" in s, s

def test_method_dispatcher_post():
    url = server() + "vikings"
    response = urlopen(url, "")
    s = response.read()
    assert s == "That was interesting.\n", s



# moin2atomentries.py - incomplete? Couldn't figure out what to test.

# moincms.py - the commented example fails, couldn't figure out what to test.

# moinrest - instructions didn't work, couldn't figure out what to test.

# oaitools - couldn't get it to work, couldn't figure out how to make it work, hence no tests.

# rdfatools.py

def test_rdfa2json():
    from amara.thirdparty import json
    url = server() + "akara.rdfa.json?url=http://zepheira.com/"
    results = json.load(urllib2.urlopen(url))
    for item in results["items"]:
        if "canonical" in item:
            assert "zepheira.com" in item["canonical"]
            break
    else:
        raise AssertionError("Could not find 'canonical'")


def test_rdfa2json_with_date():
    from amara.thirdparty import json
    url = server() + "akara.rdfa.json?url=http://www.myspace.com/parishilton"
    results = json.load(urllib2.urlopen(url))
    for item in results["items"]:
        if "canonical" in item:
            assert True
            break
    else:
        raise AssertionError("Could not find myspace:lastLogin")

# static.py

def test_static():
    # Pull up some static files
    url = server() + "resource/atom/entry1.atom"
    response = urllib2.urlopen(url)
    assert response.code == 200
    assert response.headers["Content-Type"] == "application/atom+xml", response.headers["Content-Type"]
    s = response.read()
    assert "Poster Boy @ Flickr" in s

    url = server() + "static/README"
    s = urllib2.urlopen(url).read()
    assert "SECRET MESSAGE" in s

    # Check that that leading "/" is trimmed
    url = server() + "//static////README"
    s = urllib2.urlopen(url).read()
    assert "SECRET MESSAGE" in s

def _http_failure(url, code):
    try:
        urllib2.urlopen(url).read()
        raise AssertionError("unexpected success")
    except urllib2.HTTPError, err:
        assert err.code == code, (err.code, code)

def test_static_missing_file():
    url = server() + "static/missing_file"
    _http_failure(url, 404)

# Interesting. After the upgrade to the most recent paste.httpserver
# this test fails with a 404 error instead of a 401 error. The
# new httpserver does a posixpath.normpath and converts the
# "/static/../widefinder_100.apache_log" ... to
# "/widefider_100.apache_log", which means I get a 404 error.
def test_static_bad_relative_file():
    url = server() + "static/../widefinder_100.apache_log"
    err = _http_failure(url, 404)


def test_static_unauthorized():
    url = server() + "static"
    _http_failure(url, 401)


# The simple code in the server only checks to see
# if the timestamp has changed.
_readme = os.path.join(RESOURCE_DIR, "static", "README")
_modified_since = formatdate(os.stat(_readme).st_mtime, usegmt=True)

def test_static_last_modified():
    url = server() + "static/README"
    req = urllib2.Request(url)
    req.add_header('If-Modified-Since', _modified_since)
    try:
        response = urllib2.urlopen(req)
        raise AssertionError("testing shows that this path isn't taken")
    except urllib2.HTTPError, err:
        assert err.code == 304, err.code

# statstools - needs R installed

# svntools - needs SVN installed

# unicodetools.py

def test_charbyname():
    url = server() + "akara.unicode.charbyname?name=DOUBLE+DAGGER"
    s = urllib2.urlopen(url).read()
    assert s == u"\N{DOUBLE DAGGER}".encode("utf-8")

def test_charbyname_missing():
    url = server() + "akara.unicode.charbyname?name=ETAOIN+SHRDLU"
    s = urllib2.urlopen(url).read()
    assert s == ""

def test_charsearch():
    url = server() + "akara.unicode.search?q=DAGGER"
    doc = bindery.parse(urllib2.urlopen(url))
    names = set()
    see_alsos = set()
    for child in doc.xml_select(u"characters/character"):
        names.add(child.name)
        see_alsos.add(child.see_also)
    assert names == set(["DAGGER", "DOUBLE DAGGER"]), names
    assert see_alsos == set(
        ["http://www.fileformat.info/info/unicode/char/2020/index.htm",
         "http://www.fileformat.info/info/unicode/char/2021/index.htm"]), see_alsos


# wwwlogviewer.py

_apache_query_data = open(os.path.join(RESOURCE_DIR, "widefinder_100.apache_log")).read()
def _make_log2json_request(query_args):
    from amara.thirdparty import json
    url = server() + "akara.wwwlog.json" + query_args
    req = urllib2.Request(url)
    req.add_header("Content-Type", "text/plain")
    response = urllib2.urlopen(req, _apache_query_data)
    return json.load(response)

def test_wwwlog2json():
    results = _make_log2json_request("")
    items = results["items"]
    assert len(items) == 200, len(items)
    assert items[0]["origin"] == "host-24-225-218-245.patmedia.net"
    assert items[-1]["timestamp"] == "2006-10-01T06:36:01-07:00"

def test_wwwlog2json_maxrecords():
    results = _make_log2json_request("?maxrecords=10")
    items = results["items"]
    assert len(items) == 10, len(items)
    assert items[0]["origin"] == "host-24-225-218-245.patmedia.net"
    assert items[-1]["timestamp"] == "2006-10-01T06:33:55-07:00", items[-1]["timestamp"]

def test_wwwlog2json_maxrecords_large():
    # Size is greater than the number of records
    results = _make_log2json_request("?maxrecords=1000")
    items = results["items"]
    assert len(items) == 200, len(items)

def test_wwwlog2json_nobots():
    results = _make_log2json_request("?nobots=1")
    items = results["items"]
    assert len(items) == 183, len(items)

# xslt.py
XML_DATA = open(os.path.join(RESOURCE_DIR, "xslt_spec_example.xml")).read()
XSLT_URL = iri.os_path_to_uri(os.path.join(RESOURCE_DIR, "xslt_spec_example.xslt"))
def test_xslt():
    url = server() + "akara.xslt?" + urllib.urlencode({"@xslt": XSLT_URL})
    req = urllib2.Request(url)
    req.add_header("Content-Type", "text/xml")
    response = urllib2.urlopen(req, XML_DATA)

    doc = bindery.parse(response)
    assert str(doc.html.head.title) == "Document Title", repr(str(doc.html.head.title))
    
if __name__ == "__main__":
    raise SystemExit("Use nosetests")
