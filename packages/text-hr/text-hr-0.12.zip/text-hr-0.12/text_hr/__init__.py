# package
#from word_types import *
#from base import *
import os, sys, logging

import base

MAX_WORD_LENGTH = 30

_log_fname = ""
def init_logging(fname_log):
    global _log_fname
    if _log_fname:
        logging.warning("log in %s, request to redirect to %s skipped" % (_log_fname, fname_log))
        return False
    _log_fname = os.path.join(os.path.dirname(__file__), fname_log)
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s %(levelname)-10s %(message)s',
                        filename=_log_fname,
                        filemode='w')
    logging.info("first init - log in %s" % _log_fname)
    return True


def iter_number_decl():
    for number in base.ATTR_NUMBER.values:
        for decl in base.ATTR_DECLINATION.values:
            yield number, decl

def iter_number_person():
    for number in base.ATTR_NUMBER.values:
        for person in base.ATTR_PERSON.values:
            yield number, person

def iter_number_gender():
    for number in base.ATTR_NUMBER.values:
        for gender in base.ATTR_GENDER.values:
            yield number, gender

class IterAttrs(object):
    def __init__(self, word_type_obj, suffix, suf_id, add_gender, iter_attrs, **attr_fix):
        """
        TODO: add_gender is not the best solution, callback could be better
        """
        self.iter_attrs = iter_attrs
        assert len(self.iter_attrs)==2
        self.word_type_obj = word_type_obj
        self.suffix, self.suf_id, self.add_gender = suffix, suf_id, add_gender
        for k,v in attr_fix.iteritems():
            setattr(self, k, v)

    def __iter__(self):
        """
        # NOTE: dropped - obsolete
        # >>> from nouns import NOUNS
        # >>> l = list(NOUNS.iter_suffix_cross_table())[0]
        # >>> l # doctest: +ELLIPSIS 
        # <....IterAttrs object at ...>
        # >>> l0 = list(l)
        # >>> len(l0)
        # 14
        # >>> l0[0]
        # ('S', 'N', ['$word_base0'])
        # >>> l0[-1]
        # ('P', 'I', ['%sima'])

        >>> from adjectives import ADJECTIVES
        >>> l = list(ADJECTIVES.iter_suffix_cross_table())[0]
        >>> l # doctest: +ELLIPSIS 
        <....IterAttrs object at ...>
        >>> l0 = list(l)
        >>> len(l0)
        14
        >>> l0[0]
        ('S', 'N', ['%a0'])
        >>> l0[-1]
        ('P', 'I', ['im', 'ima'])

        # >>> from verbs import VERBS
        # >>> l = list(VERBS.iter_suffix_cross_table())[0]
        # >>> l # doctest: +ELLIPSIS 
        # <....IterAttrs object at ...>
        # >>> l0 = list(l)
        # >>> len(l0)
        # 6
        # >>> l0[0]
        # ('S', '1', [u'em'])
        # >>> l0[-1]
        # ('P', '3', [u'u'])

        # >>> from verbs import VERBAL_ADJECTIVES
        # >>> l = list(VERBAL_ADJECTIVES.iter_suffix_cross_table())[0]
        # >>> l # doctest: +ELLIPSIS 
        # <....IterAttrs object at ...>
        # >>> l0 = list(l)
        # >>> len(l0)
        # 6
        # >>> l0[0]
        # ('S', 'M', [u'o'])
        # >>> l0[-1]
        # ('P', 'N', [u'la'])
        """
        import base
        for attr1 in self.iter_attrs[0].values:
            for attr2 in self.iter_attrs[1].values:
                if self.add_gender:
                    suf_values = self.suffix.suffixes["%s/%s/%s" % (attr1, attr2, self.gender)]
                else:
                    suf_values = self.suffix.suffixes["%s/%s" % (attr1, attr2)]
                yield attr1, attr2, suf_values

def test():
    print "%s: running doctests" % __name__
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test()
