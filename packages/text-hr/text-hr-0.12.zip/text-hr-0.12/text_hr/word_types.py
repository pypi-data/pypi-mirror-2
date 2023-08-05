# coding=utf-8
# type of words
# doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
"""

>>> sorted(TYPE_LIST.keys()) # doctest: +NORMALIZE_WHITESPACE
['ABBR', 'ADJ', 'ADV', 'CONJ', 'EXCL', 'N', 'NUM', 'PART', 'PREP', 
 'PRON.NEO.CH1', 'PRON.NEO.CH2', 'PRON.NEO.FIX', 'PRON.OSO', 'PRON.POK', 
 'PRON.POS', 'PRON.POV', 'PRON.PPO', 'PRON.UOD.IME', 
 'PRON.UOD.PRD', 'V']

>>> sorted(ATTR_LIST.keys()) # doctest: +NORMALIZE_WHITESPACE
['ADV_T', 'CONJ_T', 'DEC', 'EXCL_T', 'GEN', 'GRD', 'NTY', 'NUM', 'PER',
 'PER_3MFN', 'PER_MFN', 'PREP_T', 'PRON_T', 'TIM']

>>> sorted([k for k,v in TYPE_LIST.iteritems() if v.is_changeable]) # doctest: +NORMALIZE_WHITESPACE
['ADJ', 'N', 'NUM', 'PRON.NEO.CH1', 'PRON.NEO.CH2', 'PRON.OSO', 'PRON.POK', 'PRON.POS', 
 'PRON.POV', 'PRON.PPO', 'PRON.UOD.IME', 'PRON.UOD.PRD', 'V']

>>> sorted([k for k,v in TYPE_LIST.iteritems() if not v.is_changeable])
['ABBR', 'ADV', 'CONJ', 'EXCL', 'PART', 'PREP', 'PRON.NEO.FIX']


Testing all suffixes
--------------------

>>> suffixes = get_all_suffixes()

TODO: don't use suffixes directly - use word classes
#>>> len(suffixes)
#67

# >>> ", ".join(sorted([s.name for s in suffixes])) # doctest: +NORMALIZE_WHITESPACE
#     u'ADJ#P_N#, ADJ#P_N#-A#, ADJ#P_N+O#, ADJ#P_O#, 
#       N##A.M0.P-0, N##A.M0.P-0/P/G-i, N##A.M0.P-0/P/G-iju|a, 
#       N##A.M0.P-0/P/G-i|a, N##A.M0.P-ev, N##A.M0.P-ov, N##A.MOE.SN-e2, 
#       N##A.MOE.SN-e3, N##A.MOE.SN-oe, N##A.N-0, N##A.N-en, N##A.N-et, 
#       N##A.N.N, N##E.F.N-a, N##E.F.N-a/PG-%Aa, N##E.F.N-a/PG-%Ai, 
#       N##E.F.N-a/PG-%Au, N##E.F.N-a/SV-a, N##E.F.N-a/SV-e, N##EA.MOE, 
#       N##I.F.N-0, N##I.F.N-0/PG-iju, N##I.F.N-0/SI-u, 
#       PRON.NEO.CH2##sav, PRON.OSO#P/1#, PRON.OSO#P/2#vi, PRON.OSO#P/3M#, 
#       PRON.OSO#S/1#, PRON.OSO#S/2#ti, PRON.OSO#S/3F#, PRON.OSO#S/3M#, 
#       PRON.POK##ovaj, PRON.POK##ovakav, 
#       PRON.POS#P/1#na\u0161, PRON.POS#S/1#moj, PRON.POV##, 
#       PRON.UOD.IME##kakav, PRON.UOD.IME##tko, PRON.UOD.IME##\u0161to, PRON.UOD.PRD##koji, 
#       V#AOR#-h, V#AOR#-oh, V#AOR#biti, V#IMP#-ah, V#IMP#-ijah, V#IMP#-jah, 
#       V#IMV#-0, V#IMV#-i, V#IMV#biti/-i, V#PRE#-am, V#PRE#-em, V#PRE#-im, 
#       V#PRE#-jem, V#PRE#biti/NAG, V#PRE#biti/NEN, V#PRE#htjeti, 
#       V#PRE#morati/-jem, 
#       VA#ACT#-ao, VA#ACT#-o, VA#PAS#-en, VA#PAS#-jen, VA#PAS#-n, VA#PAS#-t'

Testing all words:
>>> words = get_all_std_words()

>>> len(words)
2904

>>> from morphs  import get_suff_registry

Everything is initialized
>>> print get_suff_registry()
SR(6232 suffixes, 8888 SRI objects)

NOTE: when runned directly: python word_types.py it will return: 
    SR(0 suffixes, 0 SRI objects)

ex. SR(6316 suffixes, 8888 SRI objects)
"""
import codecs, pprint, logging
import base
from   base   import _TYPE_LIST as TYPE_LIST
from   base   import _ATTR_LIST as ATTR_LIST

from nouns      import NOUNS
from adjectives import ADJECTIVES
from pronouns   import (PRONOUNS_NEO_CH1, PRONOUNS_NEO_CH2, PRONOUNS_NEO_FIX, 
                        PRONOUNS_OSO, PRONOUNS_POK, PRONOUNS_POS, PRONOUNS_POV, 
                        PRONOUNS_PPO, PRONOUNS_UOD_IME, PRONOUNS_UOD_PRD)
# in py-2.6 - numbers is module
from nums       import NUMBERS
from verbs      import VERBS
# from verbs      import VERBAL_ADJECTIVES
from fix_words  import ADVERBS, PREPOSITIONS, CONJUCTIONS, EXCLAMATIONS, PARTICLES    


# %(asctime)s 

def get_all_suffixes():
    suffixes_all = set()
    for word_type_str, word_type in TYPE_LIST.iteritems():
        if word_type.is_changeable:
            suffixes_list = word_type.suffixes_dict.values()
            for suffixes_obj in suffixes_list: 
                suffixes_all.add(suffixes_obj)
    return suffixes_all

def get_all_std_words(word_types_list=None):
    """
    TODO: explain
    htjeti               CH#V#                #PRE#NIJ#S/3#1                 'neće'
    htjeti               CH#V#                VA#ACT##P/3F#1                 'htjele'

    word_form            form descriptor
    'bi'                 'CH#biti#V#AOR#|P/3#2'
    explained:
        CH   - CH is changeable, FX is fixed
        biti - word_base
        V    - word_type_code
        AOR  - fixed attr values for this wt (separated with /)
        ''   - attr_extra value for this word form
        P/3  - changeable attr values for this wt (separated with /)
        2    - for same word form - several forms possible then counter distinguish them
    """
    import morphs
    words_all = []
    cnt_all = 0
    for word_type_str, word_type in TYPE_LIST.iteritems():
        if word_types_list and word_type_str not in word_types_list:
            continue
        if word_type.is_changeable:
            if word_type.std_words is not None: # happens to VA 
                for word_base, word_objs in word_type.std_words.iteritems():
                    if not isinstance(word_objs, (list, tuple)):
                        word_objs = [word_objs]
                    else:
                         # NOTE: currently the only case when this happens 
                         #       (two same word_bases for same word type) is in pronouns.osobne 
                         #       word_base S/2, P/3 "ona"
                         # , { "lexem" : "njo" , "word_base" : "ona"}
                         # , { "lexem" : "njim", "word_base" : "ona"}
                        pass
                    # TODO: in the case when there are more - put add descriptor in it - counter
                    for word_obj in word_objs:
                        word_base_key = "CH#%s#%s" % (word_type.code, "/".join([a for a in word_obj.attrs_fix]))

                        for suffixes_key, forms in word_obj.get_all_forms():
                            #>>> print VERBS.std_words["morati"].get_forms("PRE").pp_forms()
                            # if suffixes_key.startswith("VA#"):
                            #     assert word_type.code=="V"
                            # else:
                            assert suffixes_key.startswith(word_type.code+"#"), "%s & %s" % (suffixes_key, word_type.code)
                            # NOTE: this is not useful in tran import proc
                            # s1 = suffixes_key.split("#")
                            # s1[0]=""
                            # suffixes_key = "#".join(s1)

                            if isinstance(forms, basestring):
                                # V_ADV (glagolski pridjev prošli/sadašnji)
                                wform_key = "%s|%s#%d" % (suffixes_key, "", 1)
                                words_all.append((word_base, word_base_key, cnt_all, "", wform_key, forms))
                                cnt_all += 1
                            else:
                                suffixes_id = forms.suffixes.name
                                for form_key, wforms in forms.get_forms_ordered():
                                    assert wforms
                                    for i, wform in enumerate(wforms): 
                                        if wform:
                                            #descriptor = "CH#%s#%s|%s#%d" % (suffixes_key, form_key, i+1)
                                            wform_key = "%s|%s#%d" % (suffixes_key, form_key, i+1)
                                            words_all.append((word_base, word_base_key, cnt_all, suffixes_id, wform_key, wform ))
                                            cnt_all += 1
        else:
            for sub_type, word_set in word_type.std_words.wordset.iteritems():
                for word_base in word_set:
                    descriptor = "FX#%s#%s" % (word_type.code, sub_type)
                    words_all.append((word_base, descriptor, cnt_all, None, None, None))
                    cnt_all += 1

    return sorted(words_all)

def write_all_words_to_file(fname, cp="utf8"):
    words = get_all_std_words()
    f = codecs.open(fname, "w", cp)
    for word_base, l_key, cnt, suffixes_id, wform_key, wform  in words:
        line = u"%-20s %-20s %-20s %-30s '%s'" % (word_base, l_key, suffixes_id, wform_key, wform)
        # NOTE: this is not needed, since it is done in write function
        # line = codecs.encode(line, cp) 
        f.write(line+"\n")
    f.close()
    logging.warning("totaly %d word forms output to %s in codepage %s" % (len(words), fname, cp))

def test():
    print "%s: running doctests" % __name__
    # write_all_words_to_file("r1.txt", cp="cp1250")
    # logging.basicConfig(level=logging.DEBUG, format='%(name)-10s %(levelname)-8s:%(message)s')
    # write_all_words_to_file("r2.txt", cp="utf8")
    # write_all_words_to_file("r3.txt", cp="utf16")
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    test()

