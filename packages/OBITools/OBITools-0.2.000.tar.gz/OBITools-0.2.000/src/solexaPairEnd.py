#!/usr/local/bin/python
'''
Created on 30 dec. 2009

@author: coissac
'''

from obitools.options import getOptionManager
from obitools.fastq import fastqSolexaIterator, formatFastq
from obitools.align import QSolexaReverseAssemble
from obitools.align import QSolexaRightReverseAssemble
from obitools.tools._solexapairend import buildConsensus

def addSolexaPairEndOptions(optionManager):
    optionManager.add_option('-r','--reverse-reads',
                             action="store", dest="reverse",
                             metavar="<FILENAME>",
                             type="string",
                             default=None,
                             help="Filename containing reverse solexa reads "
                            )
    


def checkAlignOk(ali):
    #print not (ali[0][0]=='-' or ali[1][len(ali[1])-1]=='-')
    return not (ali[0][0]=='-' or ali[1][len(ali[1])-1]=='-')
    

        
def buildAlignment(direct,reverse):
    la = QSolexaReverseAssemble()
    ra = QSolexaRightReverseAssemble()
    for d in direct:
        r = reverse.next()
        la.seqA=d 
        la.seqB=r 
        ali=la()
        ali.direction='left'
        if not checkAlignOk(ali):
#            print >>sys.stderr,"-> bad : -------------------------"
#            print >>sys.stderr,ali
#            print >>sys.stderr,"----------------------------------"
            ra.seqA=d 
            ra.seqB=r
            ali=ra()
            ali.direction='right'
#            print >>sys.stderr,ali
#            print >>sys.stderr,"----------------------------------"
        yield ali
        
        
    
    
if __name__ == '__main__':
    optionParser = getOptionManager([addSolexaPairEndOptions],
                                    entryIterator=fastqSolexaIterator
                                    )
    
    (options, direct) = optionParser()
    
    reverse = fastqSolexaIterator(options.reverse)
    
    for ali in buildAlignment(direct, reverse):
        consensus = buildConsensus(ali)
        print formatFastq(consensus)
        
        

