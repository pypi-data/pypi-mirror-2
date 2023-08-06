# cython: profile=False

import re
from _fasta cimport *

_parseFastaTag=re.compile('([a-zA-Z]\w*) *= *([^;]+);')


cpdef parseFastaDescription(str ds, object tagparser=_parseFastaTag):
    
    cdef dict info
    cdef str definition
    
    info = {x:y.strip() for x,y in tagparser.findall(ds)}
    definition = tagparser.sub('',ds).strip()    

    return definition,info
