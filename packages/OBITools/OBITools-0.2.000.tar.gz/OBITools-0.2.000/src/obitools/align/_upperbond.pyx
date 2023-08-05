'''
Created on 6 Nov. 2009

@author: coissac
'''
#@PydevCodeAnalysisIgnore

from _dynamic cimport *  
from array import array
cimport array

from _upperbond cimport *
#from libupperbond import buildTable

cdef array.array[unsigned char] newtable():
    table = array.array('B',[0])
    array.resize(table,256)
    return table


def indexSequences(seq,double threshold=0.95):
    cdef bytes sequence
    cdef array.array[unsigned char] table
    cdef int overflow
    cdef int wordcount
    cdef int wordmin
    
    table = newtable() 
    sequence=bytes(str(seq))
    overflow = buildTable(sequence,table._B,&wordcount)
    wordmin = threshold4(wordcount,threshold)
    return (table,overflow,wordmin)

cpdef int countCommonWords(array.array table1,
                       int overflow1,
                       array.array table2,
                       int overflow2):
    return compareTable(table1._B,overflow1,
                        table2._B,overflow2)
 