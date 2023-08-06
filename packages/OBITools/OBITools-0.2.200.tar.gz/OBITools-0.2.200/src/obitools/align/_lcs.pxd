cdef extern from *:
    ctypedef char* const_char_ptr "const char*"
    
    
cdef import from "_lcs.h":
    int fastLCSScore(const_char_ptr seq1, const_char_ptr seq2)
