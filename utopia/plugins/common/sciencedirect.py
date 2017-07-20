import urllib2
import urlparse
import utopia.citation

from lxml import etree
from StringIO import StringIO


class ScienceDirectResolver(utopia.citation.Resolver):
    """Resolve PDF link from a Science Direct page"""

    def resolve(self, citations, document = None):
        citation = {}
        if not utopia.citation.has_link(citations, {'mime': 'application/pdf'}, {'whence': 'sciencedirect'}):
            resolved_links = utopia.citation.filter_links(citations, {'resolved_url': None})
            for link in resolved_links:
                url = link['resolved_url']
                if 'www.sciencedirect.com' in url:
                    parser = etree.HTMLParser()
                    resource = urllib2.urlopen(url, timeout=12)
                    html = resource.read()
                    dom = etree.parse(StringIO(html), parser)

                    # look for the PDF link
                    download_pdf_urls = dom.xpath('//a[@id="pdfLink"]/@href')
                    for pdf_url in download_pdf_urls:
                        pdf_url = urlparse.urljoin(url, pdf_url)
                        if pdf_url != resource.geturl(): # Check for cyclic references
                            citation.setdefault('links', [])
                            citation['links'].append({
                                'url': pdf_url,
                                'mime': 'application/pdf',
                                'type': 'article',
                                'title': 'Download article from Science Direct',
                                })
        return citation

    def provenance(self):
        return {'whence': 'sciencedirect'}

    def purposes(self):
        return 'dereference'

    def weight(self):
        return 103

