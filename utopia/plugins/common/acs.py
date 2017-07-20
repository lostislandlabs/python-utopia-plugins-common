import logging
import urllib2
import urlparse
import utopia.citation

from lxml import etree


class ACSResolver(utopia.citation.Resolver):
    """Resolve PDF link from an ACS page"""

    def resolve(self, citations, document = None):
        citation = {}
        if not utopia.citation.has_link(citations, {'mime': 'application/pdf'}, {'whence': 'acs'}):
            resolved_links = utopia.citation.filter_links(citations, {'resolved_url': None})
            for link in resolved_links:
                url = link['resolved_url']
                if 'pubs.acs.org' in url:
                    parser = etree.HTMLParser()
                    resource = urllib2.urlopen(url, timeout=12)
                    html = resource.read()
                    dom = etree.parse(StringIO(html), parser)

                    # look for the PDF link
                    download_pdf_urls = dom.xpath('//div[@class="bottomViewLinks"]/a[text()="PDF"]/@href')
                    for pdf_url in download_pdf_urls:
                        pdf_url = urlparse.urljoin(url, pdf_url)
                        if pdf_url != resource.geturl(): # Check for cyclic references
                            citation.setdefault('links', [])
                            citation['links'].append({
                                'url': pdf_url,
                                'mime': 'application/pdf',
                                'type': 'article',
                                'title': 'Download article from ACS',
                                })
        return citation

    def provenance(self):
        return {'whence': 'acs'}

    def purposes(self):
        return 'dereference'

    def weight(self):
        return 103

