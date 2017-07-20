import logging
import utopia.citation
import utopia.tools.arxiv


class ArXivExpander(utopia.citation.Resolver):
    '''From an ArXiv ID, expand the citations'''

    def resolve(self, citations, document = None):
        # If an ArXiv ID is present, look it up
        citation = {}
        arxiv_id = utopia.citation.pick_from(citations, 'identifiers[arxiv]', None, record_in=citation)
        if arxiv_id is not None:
            citation.update(utopia.tools.arxiv.resolve(arxiv_id))
        return citation

    def provenance(self):
        return {'whence': 'arxiv'}

    def purposes(self):
        return 'expand'

    def weight(self):
        return 10

