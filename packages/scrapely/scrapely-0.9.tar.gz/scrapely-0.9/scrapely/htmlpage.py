"""
htmlpage

Container objects for representing html pages and their parts in the IBL
system. This encapsulates page related information and prevents parsing
multiple times.
"""
import re
import hashlib

def create_page_from_jsonpage(jsonpage, body_key):
    """Create an HtmlPage object from a dict object conforming to the schema
    for a page

    `body_key` is the key where the body is stored and can be either 'body'
    (original page with annotations - if any) or 'original_body' (original
    page, always). Classification typically uses 'original_body' to avoid
    confusing the classifier with annotated pages, while extraction uses 'body'
    to pass the annotated pages.
    """
    url = jsonpage['url']
    headers = jsonpage.get('headers')
    body = jsonpage[body_key].decode('utf-8')
    page_id = jsonpage.get('page_id')
    encoding = jsonpage.get('encoding', 'utf-8')
    return HtmlPage(url, headers, body, page_id, encoding)

def page_to_dict(page):
    return {
        'url': page.url,
        'headers': page.headers,
        'body': page.body,
        'page_id': page.page_id,
        'encoding': page.encoding,
    }

class HtmlPage(object):
    """HtmlPage

    This is a parsed HTML page. It contains the page headers, url, raw body and parsed 
    body.

    The parsed body is a list of HtmlDataFragment objects.

    The encoding argument is the original page encoding. This isn't used by the
    core extraction code, but it may be used by some extractors to translate
    entities or encoding urls.
    """
    def __init__(self, url=None, headers=None, body=None, page_id=None, encoding='utf-8'):
        assert isinstance(body, unicode), "unicode expected, got: %s" % type(body).__name__
        self.headers = headers or {}
        self.body = body
        self.url = url or u''
        self.encoding = encoding
        if page_id is None and url:
            self.page_id = hashlib.sha1(url).hexdigest()
        else:
            self.page_id = page_id 
    
    def _set_body(self, body):
        self._body = body
        self.parsed_body = list(parse_html(body))
        
    body = property(lambda x: x._body, _set_body, doc="raw html for the page")
    
    def subregion(self, start=0, end=None):
        """HtmlPageRegion constructed from the start and end index (inclusive)
        into the parsed page
        """
        return HtmlPageParsedRegion(self, start, end)

    def fragment_data(self, data_fragment):
        """portion of the body corresponding to the HtmlDataFragment"""
        return self.body[data_fragment.start:data_fragment.end]

class HtmlPageRegion(unicode):
    """A Region of an HtmlPage that has been extracted
    """
    def __new__(cls, htmlpage, data):
        return unicode.__new__(cls, data)

    def __init__(self, htmlpage, data):
        """Construct a new HtmlPageRegion object.

        htmlpage is the original page and data is the raw html
        """
        self.htmlpage = htmlpage
    
class HtmlPageParsedRegion(HtmlPageRegion):
    """A region of an HtmlPage that has been extracted

    This has a parsed_fragments property that contains the parsed html 
    fragments contained within this region
    """
    def __new__(cls, htmlpage, start_index, end_index):
        text_start = htmlpage.parsed_body[start_index].start
        text_end = htmlpage.parsed_body[end_index or -1].end
        text = htmlpage.body[text_start:text_end]
        return HtmlPageRegion.__new__(cls, htmlpage, text)

    def __init__(self, htmlpage, start_index, end_index):
        self.htmlpage = htmlpage
        self.start_index = start_index
        self.end_index = end_index

    @property
    def parsed_fragments(self):
        """HtmlDataFragment or HtmlTag objects for this parsed region"""
        end = self.end_index + 1 if self.end_index is not None else None
        return self.htmlpage.parsed_body[self.start_index:end]

class HtmlTagType(object):
    OPEN_TAG = 1
    CLOSE_TAG = 2 
    UNPAIRED_TAG = 3

class HtmlDataFragment(object):
    __slots__ = ('start', 'end')
    
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
    def __str__(self):
        return "<HtmlDataFragment [%s:%s]>" % (self.start, self.end)

    def __repr__(self):
        return str(self)
    
class HtmlTag(HtmlDataFragment):
    __slots__ = ('tag_type', 'tag', 'attributes')

    def __init__(self, tag_type, tag, attributes, start, end):
        HtmlDataFragment.__init__(self, start, end)
        self.tag_type = tag_type
        self.tag = tag
        self.attributes = attributes

    def __str__(self):
        return "<HtmlTag tag='%s' attributes={%s} type='%d' [%s:%s]>" % (self.tag, ', '.join(sorted\
                (["%s: %s" % (k, repr(v)) for k, v in self.attributes.items()])), self.tag_type, self.start, self.end)
    
    def __repr__(self):
        return str(self)

_ATTR = "((?:[^=/<>\s]|/(?!>))+)(?:\s*=(?:\s*\"(.*?)\"|\s*'(.*?)'|([^>\s]+))?)?"
_TAG = "<(\/?)(\w+(?::\w+)?)((?:\s*" + _ATTR + ")+\s*|\s*)(\/?)>?"
_DOCTYPE = r"<!DOCTYPE.*?>"
_SCRIPT = "(<script.*?>)(.*?)(</script.*?>)"
_COMMENT = "(<!--.*?-->)"

_ATTR_REGEXP = re.compile(_ATTR, re.I | re.DOTALL)
_HTML_REGEXP = re.compile("%s|%s|%s" % (_COMMENT, _SCRIPT, _TAG), re.I | re.DOTALL)
_DOCTYPE_REGEXP = re.compile("(?:%s)" % _DOCTYPE)
_COMMENT_REGEXP = re.compile(_COMMENT, re.DOTALL)

def parse_html(text):
    """Higher level html parser. Calls lower level parsers and joins sucesive
    HtmlDataFragment elements in a single one.
    """
    # If have doctype remove it.
    start_pos = 0
    match = _DOCTYPE_REGEXP.match(text)
    if match:
        start_pos = match.end()
    prev_end = start_pos
    for match in _HTML_REGEXP.finditer(text, start_pos):
        start = match.start()
        end = match.end()
            
        if start > prev_end:
            yield HtmlDataFragment(prev_end, start)

        if match.groups()[0] is not None: # comment
            yield HtmlDataFragment(start, end)
        elif match.groups()[1] is not None: # <script>...</script>
            for e in _parse_script(match):
                yield e
        else: # tag
            yield _parse_tag(match)
        prev_end = end
    textlen = len(text)
    if prev_end < textlen:
        yield HtmlDataFragment(prev_end, textlen)

def _parse_script(match):
    """parse a <script>...</script> region matched by _HTML_REGEXP"""
    open_text, content, close_text = match.groups()[1:4]

    open_tag = _parse_tag(_HTML_REGEXP.match(open_text))
    open_tag.start = match.start()
    open_tag.end = match.start() + len(open_text)

    close_tag = _parse_tag(_HTML_REGEXP.match(close_text))
    close_tag.start = match.end() - len(close_text)
    close_tag.end = match.end()
    
    yield open_tag
    if open_tag.end < close_tag.start:
        start_pos = 0
        for m in _COMMENT_REGEXP.finditer(content):
            if m.start() > start_pos:
                yield HtmlDataFragment(open_tag.end + start_pos, open_tag.end + m.start())
            yield HtmlDataFragment(open_tag.end + m.start(), open_tag.end + m.end())
            start_pos = m.end()
        if open_tag.end + start_pos < close_tag.start:
            yield HtmlDataFragment(open_tag.end + start_pos, close_tag.start)
    yield close_tag

def _parse_tag(match):
    """
    parse a tag matched by _HTML_REGEXP
    """
    data = match.groups()
    closing, tag, attr_text = data[4:7]
    # if tag is None then the match is a comment
    if tag is not None:
        unpaired = data[-1]
        if closing:
            tag_type = HtmlTagType.CLOSE_TAG
        elif unpaired:
            tag_type = HtmlTagType.UNPAIRED_TAG
        else:
            tag_type = HtmlTagType.OPEN_TAG
        attributes = []
        for attr_match in _ATTR_REGEXP.findall(attr_text):
            name = attr_match[0].lower()
            values = [v for v in attr_match[1:] if v]
            attributes.append((name, values[0] if values else None))
        return HtmlTag(tag_type, tag.lower(), dict(attributes), match.start(), match.end())
