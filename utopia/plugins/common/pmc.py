import utopia.citation
import utopia.tools.pmc



class PMCResolver(utopia.citation.Resolver):
    """Resolve PDF link from a PMC ID"""

    def resolve(self, citations, document = None):
        citation = {}
        if not utopia.citation.has_link(citations, {'mime': 'application/pdf'}, {'whence': 'pmc'}):
            # Try to resolve the PMC ID from either the DOI or the PubMed ID
            pmcid = utopia.citation.pick_from(citations, 'identifiers/pmc', default=None)
            if pmcid is None:
                doi = utopia.citation.pick_from(citations, 'identifiers/doi', default=None, record_in=citation)
                pmid = utopia.citation.pick_from(citations, 'identifiers/pubmed', default=None, record_in=citation)
                if doi is not None and pmcid is None:
                    pmcid = utopia.tools.pmc.identify(doi, 'doi')
                if pmid is not None and pmcid is None:
                    pmcid = utopia.tools.pmc.identify(pmid, 'pmid')

            # Generate PMC link to PDF
            if pmcid is not None:
                pdf_url = 'http://www.ncbi.nlm.nih.gov/pmc/articles/{0}/pdf/'.format(pmcid)
                citation.update({
                    'links': [{
                        'url': pdf_url,
                        'mime': 'application/pdf',
                        'type': 'article',
                        'title': 'Download article from PubMed Central',
                    }],
                    'identifiers': {'pmc': pmcid}
                })
                return citation

    def provenance(self):
        return {'whence': 'pmc'}

    def purposes(self):
        return 'dereference'

    def weight(self):
        return 104


