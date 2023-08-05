from zope.interface import implements
from zope.component import queryUtility
from zope.component.interfaces import ComponentLookupError
from plone.memoize import ram
from nltk.chunk.util import tree2conlltags
from collective.classification.interfaces import IPOSTagger, ITokenizer, \
    ITermExtractor


def _extractor_cachekey(method, self, text, locale):
    return (text)


def permissiveFilter(word, occur):
    return True


class DefaultFilter(object):

    def __init__(self, minOccur=3):
        self.minOccur = minOccur

    def __call__(self, word, occur):
        return occur >= self.minOccur


class NPExtractor(object):
    implements(ITermExtractor)

    def __init__(self):
        """
        """
        self.filter = DefaultFilter()

    def _add(self, norm, terms):
        terms.setdefault(norm, 0)
        terms[norm] += 1

    @ram.cache(_extractor_cachekey)
    def extract(self, text, locale='en'):
        """
        """
        tokenizer = queryUtility(ITokenizer, name=locale)
        tagger = queryUtility(IPOSTagger, name=locale)
        if not tagger or not tokenizer:
            #Non-supported language
            return
        tokens = tokenizer.tokenize(text)
        tagged_terms = tagger.tag(tokens)
        terms = {}
        np_terms = {}
        noun_phrases = [
            node
            for node in tagger.np_grammar.parse(tagged_terms)
            if not isinstance(node, tuple)]
        for node in noun_phrases:
            coll_tag = tree2conlltags(node)
            if len(coll_tag) > 1:
                mterm = [
                    term.lower()
                    for (term, tag, temp) in coll_tag
                    if len(term)>1]
                mterm = ' '.join(mterm)
                if mterm:
                    self._add(mterm, np_terms)
            for (term, tag, temp) in coll_tag:
                if tag.startswith('N') and len(term)>1:
                    term = tagger.normalize(term, tag)
                    self._add(term.lower(), terms)
        for term in terms.keys():
            if not self.filter(term, terms[term]):
                del terms[term]
        for term in np_terms.keys():
            if not self.filter(term, np_terms[term]):
                del np_terms[term]
        return (terms, np_terms)
