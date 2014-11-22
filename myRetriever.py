from __future__ import division
from operator import itemgetter

import math
##Starts 2 classes down, wanted to keep my core class on top

class Binary:
    def __init__(self,qDoc):
        self.bDoc = []
        for docID in qDoc:
            self.bDoc.append(docID)
    def getResults(self):
        return self.bDoc[:10]
            
    
class TF:
    def __init__(self, index, qDocs, query):
        self.tf= {}

        for docID in qDocs:
             self.tf[docID] = sum(qDocs[docID].itervalues())
                
    def getTF(self):
        return self.tf

class TFIDF:
    #init class aswell working the IDF for the words relvant to query
    def __init__(self, sizeOfCollection, query, index):
        self.idfWord = {}
        self.normalized = {}
        self.query = query
 
        self.index = index
      
        for word in index:
            
             documentFreq = len(index.get(word,1))
             self.idfWord[word] = math.log10(float(sizeOfCollection)/float(documentFreq))
             for docID in self.index[word]:
               #  if word in qDocs[currentDoc]:
                 
                 if docID in  self.normalized:
                     self.normalized[docID] += (self.index[word][docID]*self.idfWord[word])**2
                 else:
                     self.normalized[docID] = (self.index[word][docID]*self.idfWord[word])**2
        for doc in self.normalized:
             self.normalized[doc] =math.sqrt(self.normalized[doc])
                     
               
               
               
    #Works out the tfIDF as well as the norm to reduce relooping    
    def termFreqIDF(self,currentDoc, qDocs):
        termFreqIDF = 0
        
        
        for word in self.query:
            if word in qDocs[currentDoc]:
                wordTfIdf = qDocs[currentDoc][word] * self.idfWord[word] 
                ##move this out
                queryScore = self.query[word]*self.idfWord[word]                
                
                termFreqIDF += (wordTfIdf * queryScore)/self.normalized[currentDoc]
      
        return termFreqIDF
  
    def getIDF(self):
        return self.idfWord
        
        
class Retrieve:
    def __init__(self,index,termWeighting):
        self.index = index
        self.termWeighting = termWeighting

    def forQuery(self,query):
      
        #gets a lits of all IDs of docs which are relvant to the query      
        (docList, qDocs) = self.findDocs(query)
        
        
        #gets a index by DocID for easier seach
       # qDocs = self.findTermsDoc(query, docList)
        scoreOfDoc = {}
        if(self.termWeighting == 'binary'):
            binary = Binary(qDocs)
            return binary.getResults()
            
        elif(self.termWeighting == 'tf'):
           
                tf = TF(self.index, qDocs, query)
                return self.sortDic(tf.getTF())
              
                
        elif(self.termWeighting == 'tfidf'):
            #gets the size of the Collection
            collectionSize = self.getCollectionSize()

            tfidf =TFIDF(collectionSize, query,self.index)
      
            for doc in qDocs:
                #tf = TF(doc, query, qDocs, docList)
                scoreOfDoc[doc] = tfidf.termFreqIDF(doc, qDocs)

                
        docrank =  self.sortDic(scoreOfDoc)
        
        return docrank
##pulls out all relvant docs for the query to reduce search time.
    def findDocs(self,query):
        docs = []
        qDocs = {}       
          
        for word in query:
           # print word
            #print self.index.get(word,1)
            if word in self.index:
                for docid in self.index[word]:
                    if docid not in docs:
                        docs.append(docid)
                    if docid in qDocs:
                        qDocs[docid][word] = self.index[word][docid]
                    else:
                        qDocs[docid]= {}
                        qDocs[docid][word] = self.index[word][docid]
                        
                        
                        
                        
        return (sorted(docs), qDocs)

##returns size of Collection    
    def getCollectionSize(self):
        maxID = 0
        for word in self.index:
             newID = max(self.index.get(word,1), key = self.index.get(word,1).get)
             if newID > maxID:
                 maxID = newID
            
      
        return maxID
##Sorts Dic based on score and returns top 10        
    def sortDic(self, dic):
       
        sortedx =  sorted(dic.items(), key=itemgetter(1), reverse=True)[:10]
        sortedToArray = []
        for docs in sortedx:
            sortedToArray.append(docs[0])
            
       
        return sortedToArray



