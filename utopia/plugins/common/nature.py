import urllib2
import urlparse
import utopia.citation

from lxml import etree
from StringIO import StringIO


class NatureResolver(utopia.citation.Resolver):
    """Resolve PDF link from a Nature page"""

    def resolve(self, citations, document = None):
        citation = {}
        if not utopia.citation.has_link(citations, {'mime': 'application/pdf'}, {'whence': 'nature'}):
            resolved_links = utopia.citation.filter_links(citations, {'resolved_url': None})
            for link in resolved_links:
                url = link['resolved_url']
                if 'www.nature.com' in url:
                    parser = etree.HTMLParser()
                    resource = urllib2.urlopen(url, timeout=12)
                    html = resource.read()
                    dom = etree.parse(StringIO(html), parser)
                    # look for the PDF link
                    download_pdf_urls = dom.xpath('//li[@class="download-pdf"]/a/@href')
                    for pdf_url in download_pdf_urls:
                        pdf_url = urlparse.urljoin(url, pdf_url)
                        if pdf_url != resource.geturl(): # Check for cyclic references
                            citation.setdefault('links', [])
                            citation['links'].append({
                                'url': pdf_url,
                                'mime': 'application/pdf',
                                'type': 'article',
                                'title': 'Download article from Nature',
                                })
                    # look for the supplementary PDF link(s)
                    for supp in dom.xpath('//div[@id="supplementary-information"]//dl'):
                        download_supp_pdf_urls = supp.xpath('//dt/a/@href')
                        for pdf_url in download_supp_pdf_urls:
                            pdf_url = urlparse.urljoin(url, pdf_url)
                            if pdf_url != resource.geturl(): # Check for cyclic references
                                citation.setdefault('links', [])
                                citation['links'].append({
                                    'url': pdf_url,
                                    'mime': 'application/pdf',
                                    'type': 'supplementary',
                                    'title': 'Download supplementary information from Nature',
                                    })
        return citation

    def provenance(self):
        return {'whence': 'nature'}

    def purposes(self):
        return 'dereference'

    def weight(self):
        return 103


