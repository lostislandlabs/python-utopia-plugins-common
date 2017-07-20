import re
import utopia.citation
import utopia.tools.pubmed



class PubMedIdentifier(utopia.citation.Resolver):
    '''Given information, try to identify the document in the PubMed database.'''

    def resolve(self, citations, document = None):
        citation = {}
        pubmed_id = utopia.citation.pick_from(citations, 'identifiers[pubmed]', None, record_in=citation)
        if pubmed_id is None:
            doi = utopia.citation.pick_from(citations, 'identifiers[doi]', None, record_in=citation)
            if doi is not None:
                pubmed_id = utopia.tools.pubmed.identify(doi, 'doi')
                if pubmed_id is not None:
                    citation['identifiers'] = {'pubmed': pubmed_id}
            if pubmed_id is None:
                title = utopia.citation.pick_from(citations, 'title', None, record_in=citation)
                if title is not None:
                    title = title.strip(' .')
                    pubmed_results = utopia.tools.pubmed.search(title)
                    pubmed_title = pubmed_results.get('title', '').strip(' .')
                    if len(pubmed_title) > 0:
                        matched = False
                        pubmed_pmid = pubmed_results.get('identifiers', {}).get('pubmed')
                        if re.sub(r'[^\w]+', ' ', title).strip().lower() == re.sub(r'[^\w]+', ' ', pubmed_title).strip().lower(): # Fuzzy match
                            matched = True
                        elif document is not None:
                            # Accept the pubmed title over the scraped title, if present in the document
                            matches = document.findInContext('', pubmed_title, '') # Fuzzy match
                            if len(matches) > 0:
                                matched = True
                                pubmed_title = matches[0].text()
                        if matched:
                            citation.update(pubmed_results)
                            citation['title'] = pubmed_title

        return citation

    def provenance(self):
        return {'whence': 'pubmed'}

    def purposes(self):
        return 'identify'

    def weight(self):
        return 1


class PubMedExpander(utopia.citation.Resolver):
    '''From a PubMed ID, expand the citations'''

    def resolve(self, citations, document = None):
        # If a PubMed ID is present, look it up
        citation = {}
        pmid = utopia.citation.pick_from(citations, 'identifiers[pubmed]', default=None, record_in=citation)
        title = utopia.citation.pick_from(citations, 'title:pubmed', default=None)
        if title is None and pmid is not None:
            citation.update(utopia.tools.pubmed.resolve(pmid))
        return citation

    def provenance(self):
        return {'whence': 'pubmed'}

    def purposes(self):
        return 'expand'

    def weight(self):
        return 11


class PubMedResolver(utopia.citation.Resolver):
    """Resolve a URL from a PubMed ID"""

    def resolve(self, citations, document = None):
        citation = {}
        # If a PubMed ID is present, but no PubMed link, we can generate one
        pmid = utopia.citation.pick_from(citations, 'identifiers[pubmed]', default=None, record_in=citation)
        if pmid is not None and not utopia.citation.has_link(citations, {'type': 'abstract'}, {'whence': 'pubmed'}):
            citation['links'] = [{
                'url': 'http://www.ncbi.nlm.nih.gov/pubmed/{0}'.format(pmid),
                'mime': 'text/html',
                'type': 'abstract',
                'title': 'Show in PubMed',
            }]
        return citation

    def provenance(self):
        return {'whence': 'pubmed'}

    def purposes(self):
        return 'dereference'

    def weight(self):
        return 101
