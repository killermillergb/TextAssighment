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
    def __init__(self, currentDoc, query, qDocs):
        self.tf = {}
        for word in query:
            self.tf[currentDoc]
            if word in qDocs[currentDoc]:
                self.tf = qDocs[currentDoc][word] * query[word] 
                
    def getTF(self):
        return (self.tf)

class TFIDF:
    #init class aswell working the IDF for the words relvant to query
    def __init__(self, docList, query, sizeOfCollection, index):
       
        self.query = query
        
        documentFreq = {}
        #collectionFreq = {}
        self.idfWord = {}
        tfIdfWord= {}
        #add words to dic
        for word in self.query:
            documentFreq[word]=0
        #   collectionFreq[word]=0
            self.idfWord[word]=0
            tfIdfWord[word]=0
                        
        for word in self.query:
             if word in index:
                 wordIDs = index.get(word,1)
                 
                 documentFreq[word] = len(wordIDs)
        #         for wordDocID in wordDocIDs:
        #             collectionFreq[word] += wordDocIDs[wordDocID]
        for word in self.query:
            if documentFreq[word] == 0:
                self.idfWord[word] = 0
            else:
                self.idfWord[word] = math.log10(float(sizeOfCollection)/float(documentFreq[word]))
    #Works out the tfIDF as well as the norm to reduce relooping    
    def termFreqIDF(self,currentDoc, qDocs):
        termFreqIDF = 0
        normDoc = 0
        for word in self.query:
            if word in qDocs[currentDoc]:
                wordTfIdf = qDocs[currentDoc][word] * self.idfWord[word] 
                
                normDoc += math.pow(wordTfIdf,2)
                queryScore = self.query[word]*self.idfWord[word]                
                
                termFreqIDF += wordTfIdf * queryScore
      
        return (termFreqIDF, math.sqrt(normDoc))
    def normalizeDoc(self, index, docList):
        normDoc = {}
        for docID in docList:
            noramDoc[docID] = 0
            for i in index:
                if docID in i:
                    noramDoc[docID] += index[word][docID]
            
        
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
            for doc in qDocs:
                tf = TF(doc, query, qDocs)
                scoreOfDoc[doc] = tf.getTF()
                
                
        elif(self.termWeighting == 'tfidf'):
           
            tfidf =TFIDF(docList, query, collectionSize, self.index )
            for doc in qDocs:
                tf = TF(doc, query, qDocs)
                (termFreqIDF, normDoc)= tfidf.termFreqIDF(doc, qDocs)
               
                scoreOfDoc[doc] =  float(termFreqIDF)/float(normDoc)
                
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
                       
        print  sorted(docs)
        return sorted(docs)
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

        
        
    
#    def normalizeQuery(self, query, idfWord):
#        queryN = 0
#        for word in query:
#            q = (query[word] * idfWord[word])
#            queryN += math.pow(q,2)
#       
#        return math.sqrt(queryN)



