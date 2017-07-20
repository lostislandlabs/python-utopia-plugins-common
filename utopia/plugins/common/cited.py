import json
import hashlib
import urllib2
import utopia.citation
import utopia.tools.cited

class CitedUnstructuredIdentifier(utopia.citation.Resolver):
    '''Give unstructured citations a hash identifier'''

    def resolve(self, citations, document = None):
        # Get all the citations that are unstructured
        for citation in citations:
            unstructured = utopia.citation.pick(citation, 'unstructured', default=None)
            if unstructured is not None:
                # Hash the unstructured text
                unstructured = unstructured.strip()
                print('Found unstructured: {}'.format(repr(unstructured)))
                hash = hashlib.sha256(unstructured.encode('utf8')).hexdigest()
                print('Generated hash: {}'.format(hash))
                utopia.citation.set_by_keyspec(citation, 'identifiers[unstructured]', hash)

    def purposes(self):
        return 'identify'

    def weight(self):
        return -9200

class CitedResolver(utopia.citation.Resolver):
    '''Submit citation identifiers to cited for resolution'''

    def resolve(self, citations, document = None):
        identifiers = utopia.citation.pick_from(citations, 'identifiers', default={})
        if len(identifiers) > 0:
            return utopia.tools.cited.resolve(**identifiers)

    def purposes(self):
        return 'identify'

    def weight(self):
        return -9100

class CitedParser(utopia.citation.Resolver):
    '''Submit unstructured citations to cited for parsing'''

    def resolve(self, citations, document = None):
        # Multiple responses leads to a no-op
        for citation in citations:
            if utopia.citation.pick(citation, 'provenance/whence', default=None) == 'cermine':
                # Bail if cermine results are already present
                return None

        # Get all the citations that don't look structured
        structure_keys = set(['title', 'authors', 'year'])
        citation = {}
        unstructured = utopia.citation.pick_from(citations, 'unstructured', default=None, record_in=citation)
        if unstructured is not None and len(structure_keys & set(unstructured.citation.keys())) == 0:
            structured = utopia.tools.cited.parse(unstructured)
            if len(structured) > 0:
                citation.update(structured[0])
                return citation

    def purposes(self):
        return 'identify'

    def weight(self):
        return -9000

class CitedSubmitter(utopia.citation.Resolver):
    '''Submit citation information to cited'''

    def resolve(self, citations, document = None):
        utopia.tools.cited.submit(citations)

    def provenance(self):
        return {'whence': 'cited'}

    def purposes(self):
        return 'dereference'

    def weight(self):
        return 100000
