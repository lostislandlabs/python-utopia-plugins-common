import urllib2
import urlparse
import utopia.citation

from lxml import etree
from StringIO import StringIO


class WileyResolver(utopia.citation.Resolver):
    """Resolve PDF link from a Wiley page"""

    def resolve(self, citations, document = None):
        citation = {}
        if not utopia.citation.has_link(citations, {'mime': 'application/pdf'}, {'whence': 'wiley'}):
            pdf_links = utopia.citation.filter_links(citations, {'mime': 'application/pdf'})
            for link in pdf_links:
                url = link['url']
                if 'onlinelibrary.wiley.com' in url:
                    parser = etree.HTMLParser()
                    resource = urllib2.urlopen(url, timeout=12)
                    html = resource.read()
                    dom = etree.parse(StringIO(html), parser)
                    # look for the PDF link
                    download_pdf_urls = dom.xpath('//iframe[@id="pdfDocument"]/@src')
                    for pdf_url in download_pdf_urls:
                        pdf_url = urlparse.urljoin(url, pdf_url)
                        if pdf_url != resource.geturl(): # Check for cyclic references
                            citation.setdefault('links', [])
                            citation['links'].append({
                                'url': pdf_url,
                                'mime': 'application/pdf',
                                'type': 'article',
                                'title': 'Download article from Wiley',
                                })
        return citation

    def provenance(self):
        return {'whence': 'wiley'}

    def purposes(self):
        return 'dereference'

    def weight(self):
        return 103

