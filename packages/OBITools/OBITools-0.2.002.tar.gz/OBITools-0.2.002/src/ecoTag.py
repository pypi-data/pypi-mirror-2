#!/usr/local/bin/python

from obitools.fasta import fastaNucIterator,formatFasta
from obitools.align.ssearch import ssearchIterator
from obitools.utils.bioseq import uniqSequence,sortSequence

from obitools.options.taxonomyfilter import addTaxonomyDBOptions,loadTaxonomyDatabase


from obitools.options import getOptionManager


def addSearchOptions(optionManager):
    
    optionManager.add_option('-R','--ref-database',
                             action="store", dest="database",
                             metavar="<FILENAME>",
                             type="string",
                             help="fasta file containing reference"
                                  "sequences")
        
    optionManager.add_option('-s','--shape',
                             action="store", dest="shape",
                             metavar="shapeness",
                             type="float",
                             default=2.0,
                             help="selectivity on the ssearch results "
                                  "1.0 is the higher selectivity."
                                  "value > 1.0 decrease selectivity.")
    
    optionManager.add_option('-c','--coverage',
                             action="store", dest="mincov",
                             metavar="min_cov",
                             type="float",
                             default=0.9,
                             help="minimum ratio between match length and"
                                  " query length . c in [0.0,1.0]  default = 0.9.")
    
    optionManager.add_option('-C','--db-coverage',
                             action="store", dest="dbcov",
                             metavar="db_cov",
                             type="float",
                             default=0.9,
                             help="minimum ratio between match length and"
                                  " subject length . C in [0.0,1.0] default = 0.9.")
    
    optionManager.add_option('-p','--program',
                             action="store", dest="program",
                             metavar="fasta35|ssearch35",
                             type="string",
                             default='fasta35',
                             help="Program used for search similarity.")
    
    optionManager.add_option('-x','--explain',
                             action='store',dest='explain',
                             type="string",
                             default=None,
                             help="Add in the output CD (complementary data) record "
                                  "to explain identification decision")
    
    optionManager.add_option('-u','--uniq',
                             action='store_true',dest='uniq',
                             default=False,
                             help='Apply uniq filter on sequences before identification')
    
    optionManager.add_option('-T','--table',
                             action='store_true',dest='table',
                             default=False,
                             help='Write results in a tabular format')
    
    optionManager.add_option('-S','--sort',
                             action='store',dest='sort',
                             type='string',
                             default=None,
                             help='Sort output on input sequence tag')
    
    optionManager.add_option('-r','--reserse',
                             action='store_true',dest='reverse',
                             default=False,
                             help='Sort in reverse order (should be used with -S)')
    
    optionManager.add_option('-o','--output-sequence',
                             action='store_true',dest='sequence',
                             default=False,
                             help='Add an extra column in the output with the query sequence')
    
    
    

def ssearchPropsFilter(ssearchresult,shape=2.0,coverage=0.9,dbcoverage=0.9):
    try:
        idmax = ssearchresult.props[0]['identity']
    except AttributeError:
        return None

    idthresold = idmax ** shape
    
    fprops = [x for x in ssearchresult.props
              if x['identity']>=idthresold
                 and (float(x['matchlength'])/ssearchresult.queryLength) >= coverage
                 and (float(x['matchlength'])/float(x['subjectlength'])) >= dbcoverage]
        
    return fprops 

def count(data):
    rep = {}
    for x in data:
        if isinstance(x, (list,tuple)):
            k = x[0]
            if len(x) > 1:
                v = [x[1]]
                default=[]
            else:
                v = 1
                default=0
        else:
            k=x
            v=1
            default=0
        rep[k]=rep.get(k,default)+v
    return rep

if __name__=='__main__':
    
    optionParser = getOptionManager([addSearchOptions,addTaxonomyDBOptions],
                                    entryIterator=fastaNucIterator
                                    )
    
    (options, entries) = optionParser()
    
    assert options.program in ('fasta35','ssearch35')
    
    if options.explain is not None:
        options.table=True

    taxonomy = loadTaxonomyDatabase(options)
    
    db = fastaNucIterator(options.database)
    taxonlink = {}

    rankid = taxonomy.findRankByName(options.explain)
    
    for seq in db:
        id = seq.id[0:46]
        assert id not in taxonlink
        taxonlink[id]=int(seq['taxid'])
        
        
    if options.uniq:
        entries = uniqSequence(entries)
        
    if options.sort is not None:
        entries = sortSequence(entries, options.sort, options.reverse)

    search = ssearchIterator(entries,
                             options.database,
                             program=options.program,
                             opts='-r"+10/-8" -f4 -n -H -m9 -d0 -b100 -q @')
                             
    for seq,match in search:
        good = ssearchPropsFilter(match,options.shape,options.mincov,options.dbcov)
        try:
            seqcount = seq['count']
        except KeyError:
            seqcount=1

        if good:
            taxlist = set(taxonlink[p['ac']] for p in good)
            lca = taxonomy.lastCommonTaxon(*tuple(taxlist))
            scname = taxonomy.getScientificName(lca)
            rank = taxonomy.getRank(lca)
      
            species = taxonomy.getSpecies(lca)
            if species is not None:
                spname = taxonomy.getScientificName(species)
            else:
                spname = '--'
                species= '-1'
      
            genus = taxonomy.getGenus(lca)
            if genus is not None:
                gnname = taxonomy.getScientificName(genus)
            else:
                gnname = '--'
                genus= '-1'
                
            order = taxonomy.getOrder(lca)
            if order is not None:
                orname = taxonomy.getScientificName(order)
            else:
                orname = '--'
                order= '-1'
                
            family = taxonomy.getFamily(lca)
            if family is not None:
                faname = taxonomy.getScientificName(family)
            else:
                faname = '--'
                family= '-1'
                
                
    
            data =['ID',match.query,good[0]['ac'],good[0]['identity'],good[-1]['identity'],'%4.3f' %(good[0]['identity']**options.shape),seqcount,len(good),lca,scname,rank,order,orname,family,faname,genus,gnname,species,spname]
        else:
            data =['UK',match.query,'--','--','--','--',seqcount,0,1,'root','no rank','-1','--','-1','--','-1','--','-1','--']
            
        if options.sequence:
            data.append(seq)
            
        if options.table:
            print '\t'.join([str(x) for x in data])
        else:
            seq['id_status']=data[0]=='ID'
            seq['count']=data[6]
            seq['match_count']=data[7]
            seq['taxid']=data[8]
            seq['scientific_name']=data[9]
            seq['rank']=data[10]
            if seq['id_status']:
                seq['better_match']=data[2]
                seq['better_identity']=data[3]
                seq['worst_identity']=data[4]
                seq['lower_id_limit']=float(data[5])
                if int(data[11])>=0:
                    seq['order']=data[11]
                    seq['order_name']=data[12]
                if int(data[13])>=0:
                    seq['family']=data[13]
                    seq['family_name']=data[14]
                if int(data[15])>=0:
                    seq['genus']=data[15]
                    seq['genus_name']=data[16]
                if int(data[17])>=0:
                    seq['species']=data[17]
                    seq['species_name']=data[18]
            print formatFasta(seq)        
                
        
        if good and rankid is not None:
            splist=count((taxonomy.getTaxonAtRank(x, rankid),y) 
                         for x,y in ((taxonlink[p['ac']],p['identity']) for p in good))
            if None in splist:
                del splist[None]
            data=[]
            for taxon in splist:
                scname = taxonomy.getScientificName(taxon)
                species=taxonomy.getSpecies(taxon)
                countt = len(splist[taxon])
                mini = min(splist[taxon])
                maxi = max(splist[taxon])
                if species is not None:
                    spname = taxonomy.getScientificName(species)
                else:
                    spname = '--'
                    species= '-1'
          
                genus = taxonomy.getGenus(taxon)
                if genus is not None:
                    gnname = taxonomy.getScientificName(genus)
                else:
                    gnname = '--'
                    genus= '-1'
                    
                order = taxonomy.getOrder(taxon)
                if order is not None:
                    orname = taxonomy.getScientificName(order)
                else:
                    orname = '--'
                    order= '-1'
                    
                family = taxonomy.getFamily(taxon)
                if family is not None:
                    faname = taxonomy.getScientificName(family)
                else:
                    faname = '--'
                    family= '-1'


                data.append(['CD',match.query,'--',maxi,mini,'--','--',countt,taxon,scname,options.explain,order,orname,family,faname,genus,gnname,species,spname])
            data.sort(lambda x,y:cmp(y[2], x[2]))    
            for d in data:
                if options.sequence:
                    d.append('--')
                print '\t'.join([str(x) for x in d])
                