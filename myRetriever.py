from __future__ import division
from operator import itemgetter

import math
##Starts 2 classes down, wanted to keep my core class on top
class Binary:
    def __init__(self, index, docList, query):
        self.qDocs = {}        
        for docIDs in docList:
            self.qDocs[docIDs]=0
            
        for word in query:
            #if the word is not in index catch error
            if word in index:
                wordDocIDs = index.get(word,1)
            
                for wordDocID in wordDocIDs:

                        self.qDocs[wordDocID] += 1
    def getBinary(self):
        return self.qDocs

class TF:
    def __init__(self, index, qDocs, query):
        self.qDocs = {}        
        for docIDs in qDocs:
            self.qDocs[docIDs]=0
            
        for word in query:
            #if the word is not in index catch error
            if word in index:
                wordDocIDs = index.get(word,1)
            
                for wordDocID in wordDocIDs:

                        self.qDocs[wordDocID] +=  index[word][wordDocID]
                
    def getTF(self):
        return (self.qDocs)

class TFIDF:
    #init class aswell working the IDF for the words relvant to query
    def __init__(self, sizeOfCollection, query, index, docList):
        self.idfWord = {}
        self.query = query
        self.docList = docList
        self.index = index
        for word in index:
                 documentFreq = len(index.get(word,1))
                 self.idfWord[word] = math.log10(float(sizeOfCollection)/float(documentFreq))
        self.normalized = self.normalizeDoc()
               
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
        
    def normalizeDoc(self):
        self.normDoc = {}
        for docID in self.docList:
            self.normDoc[docID] = 0
            for i in self.index:
           
                if docID in self.index[i]:
                
                   
                    self.normDoc[docID] += (self.index[i][docID]*self.idfWord[i])**2
                  
      
        for doc in self.normDoc:
            self.normDoc[doc] =math.sqrt(self.normDoc[doc])
        return self.normDoc
            
        
    def getIDF(self):
        return self.idfWord
        
        
class Retrieve:
    def __init__(self,index,termWeighting):
        self.index = index
        self.termWeighting = termWeighting

    def forQuery(self,query):
      
        #gets a lits of all IDs of docs which are relvant to the query      
        docList = self.findDocs(query)
        #gets the size of the Collection
        collectionSize = self.getCollectionSize()
        #gets a index by DocID for easier seach
        qDocs = self.findTermsDoc(query, docList)
        scoreOfDoc = {}
        
        
        if(self.termWeighting == 'binary'):
            binary = Binary(self.index, docList, query)
            return self.sortDic(binary.getBinary())
            
        elif(self.termWeighting == 'tf'):
           
                tf = TF(self.index, qDocs, query)
                return self.sortDic(tf.getTF())
              
                
        elif(self.termWeighting == 'tfidf'):
         
            tfidf =TFIDF(collectionSize, query,self.index, docList )
      
            for doc in qDocs:
                #tf = TF(doc, query, qDocs, docList)
                scoreOfDoc[doc] = tfidf.termFreqIDF(doc, qDocs)

                
        docrank =  self.sortDic(scoreOfDoc)
        
        return docrank
##pulls out all relvant docs for the query to reduce search time.
    def findDocs(self,query):
        docs = []  
          
        for word in query:
           # print word
            #print self.index.get(word,1)
            if word in self.index:
                docwd = self.index.get(word,1)
           
            
                for docid in docwd:
                   
                    if docid not in docs:
                        docs.append(docid)
                       
      
        return sorted(docs)
        
##indexes by docID to make easier access for searching by docID
##Could keep it as word index but i perfer it my way
    def findTermsDoc(self,query , docList):
        qDocs = {}        
        for docIDs in docList:
            qDocs[docIDs]={}
            
        for word in query:
            #if the word is not in index catch error
            if word in self.index:
                wordDocIDs = self.index.get(word,1)
            
                for wordDocID in wordDocIDs:

                        qDocs[wordDocID][word] = wordDocIDs[wordDocID]
                
         
        return qDocs 
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
            
        print sortedToArray
        return sortedToArray



        
        
    
#    def normalizeQuery(self, query, idfWord):
#        queryN = 0
#        for word in query:
#            q = (query[word] * idfWord[word])
#            queryN += math.pow(q,2)
#       
#        return math.sqrt(queryN)



