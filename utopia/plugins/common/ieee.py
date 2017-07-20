import urllib2
import urlparse
import utopia.citation

from lxml import etree
from StringIO import StringIO


class IEEEResolver(utopia.citation.Resolver):
    """Resolve PDF link from an IEEE page"""

    def resolve(self, citations, document = None):
        citation = {}
        if not utopia.citation.has_link(citations, {'mime': 'application/pdf'}, {'whence': 'ieee'}):
            resolved_links = utopia.citation.filter_links(citations, {'resolved_url': None})
            for link in resolved_links:
                url = link['resolved_url']
                if 'ieeexplore.ieee.org' in url:
                    parser = etree.HTMLParser()
                    resource = urllib2.urlopen(url, timeout=12)
                    html = resource.read()
                    dom = etree.parse(StringIO(html), parser)

                    # look for the PDF link
                    download_pdf_urls = dom.xpath('//a[@id="full-text-pdf"]/@href')
                    for pdf_url in download_pdf_urls:
                        pdf_url = urlparse.urljoin(url, pdf_url)
                        if pdf_url != resource.geturl(): # Check for cyclic references
                            # follow the link and find the iframe src
                            resource = urllib2.urlopen(pdf_url, timeout=12)
                            html = resource.read()
                            dom = etree.parse(StringIO(html), parser)

                            # developing time-frequency features for prediction
                            download_pdf_urls = dom.xpath("//frame[contains(@src, 'pdf')]/@src")
                            for pdf_url in download_pdf_urls:
                                pdf_url = urlparse.urljoin(url, pdf_url)
                                citation.setdefault('links', [])
                                citation['links'].append({
                                    'url': pdf_url,
                                    'mime': 'application/pdf',
                                    'type': 'article',
                                    'title': 'Download article from IEEEXplore',
                                    })
        return citation

    def provenance(self):
        return {'whence': 'ieee'}

    def purposes(self):
        return 'dereference'

    def weight(self):
        return 103

