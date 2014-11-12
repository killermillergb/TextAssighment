
import sys, getopt, re
import myRetriever

class CommandLine:
    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1:],'hspw:o:')
        opts = dict(opts)

        if '-h' in opts:
            self.printHelp()

        if len(args) > 0:
            print >> sys.stderr, "\n*** ERROR: no arg files - only options! ***"
            self.printHelp()

        if '-w' in opts:
            if opts['-w'] in ('binary','tf','tfidf'):
                self.termWeighting = opts['-w']
            else:
                print >> sys.stderr, "\n*** ERROR: term weighting label (opt: -w LABEL) not recognised! ***"
                print >> sys.stderr, " -- must be one of: binary / tf / tfidf"
                self.printHelp()
        else:
            self.termWeighting = 'binary'

        if '-o' in opts:
            self.outstream = open(opts['-o'],'w')
        else:
            self.outstream = sys.stdout

        if '-s' in opts and '-p' in opts:
            self.indexFile = 'index_withstoplist_withstemming.txt'
            self.queriesFile = 'queries_withstoplist_withstemming.txt'
        elif '-s' in opts:
            self.indexFile = 'index_withstoplist_nostemming.txt'
            self.queriesFile = 'queries_withstoplist_nostemming.txt'
        elif '-p' in opts:
            self.indexFile = 'index_nostoplist_withstemming.txt'
            self.queriesFile = 'queries_nostoplist_withstemming.txt'
        else:
            self.indexFile = 'index_nostoplist_nostemming.txt'
            self.queriesFile = 'queries_nostoplist_nostemming.txt'

    def printHelp(self,stream=sys.stderr):
        help = """\
        \nUSE: python %s (options)\
        \nOPTIONS:\
        \n    -h : print this help message\
        \n    -s : use "with stoplist" configuration (default: without)\
        \n    -p : use "with stemming" configuration (default: without)\
        \n    -w LABEL : use weighting scheme "LABEL" (LABEL in {binary, tf, tfidf}, default: binary)\
        \n    -o FILE : output results to file FILE (default: output to stdout)\
        """
        print >> stream, '-' * 77,
        print >> stream, help % sys.argv[0]
        print >> stream, '-' * 77
        exit()
        
class Queries:
    def __init__(self,queriesFile):
        self.qStore = {}
        termCountRE = re.compile('(\w+):(\d+)')
        f = open(queriesFile,'r')
        for line in f:
            
        
            qid = int(line.split(' ',1)[0])
            self.qStore[qid] = {}
            for (term,count) in termCountRE.findall(line):
                self.qStore[qid][term] = int(count)
    
    def getQuery(self,qid):
        if qid in self.qStore:
            return self.qStore[qid]
        else:
            print >> sys.stderr, "\n*** ERROR: unknown query identifier (\"%s\") ***" % qid
            if type(qid) == type(''):
                print >> sys.stderr, 'WARNING: query identifiers should be of type: integer'
                print >> sys.stderr, '         -- your query identifier is of type: string'
            print >> sys.stderr, ' -- program exiting'
    
    def qids(self):
        return sorted(self.qStore.keys())

class IndexLoader:
    def __init__(self,indexFile):
        self.index = {}
        docidCountRE = re.compile('(\d+):(\d+)')
        f = open(indexFile,'r')
        for line in f:
            term = line.split(' ',1)[0]
            self.index[term] = {}
            for (docid,count) in docidCountRE.findall(line):
                docid = int(docid)
                self.index[term][docid] = int(count)

    def getIndex(self):
        return self.index

class ResultStore:
    def __init__(self,outstream):
        self.outstream = outstream
        self.results = []

    def store(self,qid,docids):
        if len(docids) > 10:
            docids = docids[:10]
        self.results.append((qid,docids))

    def output(self):
        for (qid,docids) in self.results:
            for docid in docids:
                print >> self.outstream, qid, docid
            #    print queries.getQuery(qid)

    
if __name__ == '__main__':

    config = CommandLine()
    indexLoader = IndexLoader(config.indexFile)
    index = indexLoader.getIndex()
    retrieve = myRetriever.Retrieve(index,config.termWeighting)
    queries = Queries(config.queriesFile)
    allResults = ResultStore(config.outstream)


    for qid in queries.qids():
        query = queries.getQuery(qid)
        results = retrieve.forQuery(query)
        allResults.store(qid,results)
        
    allResults.output()
