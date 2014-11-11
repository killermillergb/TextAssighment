from operator import itemgetter
import math

class Retrieve:
    def __init__(self,index,termWeighting):
        self.index = index
        self.termWeighting = termWeighting

    def forQuery(self,query):
        
        #find docs that are relvent for search
        #reduces wasted search time
        docList = self.findDocs(query)
        #print docList
        
        collectionSize = self.getCollectionSize()
        qDocs = self.findTermsDoc(query, docList)
        iDF =self.inverseDocumentFrequency(docList, query, collectionSize)
        #print qDocs



        scoreOfDoc = {}
        normQ =self.normalizeQuery(query,iDF)
   
        for doc in qDocs:
             #print doc
             (termFreqIDF, normDoc)= self.termFreqIDF(doc, query, iDF, qDocs)
             if normQ == 0 or normDoc == 0:
                  scoreOfDoc[doc] = 0
             else:
                  scoreOfDoc[doc] =  termFreqIDF/(normQ * normDoc)
       
        docrank =  self.sortDic(scoreOfDoc)
        
        
        
        
       
        return docrank




    def findTermsDoc(self,query , docList):
        qDocs = {}        
        for docIDs in docList:
            qDocs[docIDs]={}
            
        for word in query:
            #if the word is not in index catch error
            if word in self.index:
                wordDocIDs = self.index.get(word,1)
            
                for wordDocID in wordDocIDs:
                    if(wordDocID, word) in qDocs:
                        qDocs[wordDocID][word] += wordDocIDs[wordDocID]
                    elif wordDocID in qDocs:
                        qDocs[wordDocID][word] = wordDocIDs[wordDocID]
                    else:
                        #this should never happen, but just in case
                        print "error DocID was never added"
         
        return qDocs 
    def inverseDocumentFrequency(self, docList, query, sizeOfCollection):
       
        
        documentFreq = {}
        #collectionFreq = {}
        idfWord = {}
        tfIdfWord= {}
        #add words to dic
        for word in query:
            documentFreq[word]=0
        #   collectionFreq[word]=0
            idfWord[word]=0
            tfIdfWord[word]=0
                        
        for word in query:
             if word in self.index:
                 wordDocIDs = self.index.get(word,1)
                 
                 documentFreq[word] = len(wordDocIDs)
        #         for wordDocID in wordDocIDs:
        #             collectionFreq[word] += wordDocIDs[wordDocID]
        for word in query:
            if documentFreq[word] == 0:
                idfWord[word] = 0
            else:
                idfWord[word] = math.log10(sizeOfCollection/documentFreq[word])
        

                
        
        return idfWord
    def normalizeQuery(self, query, idfWord):
        queryN = 0
        for word in query:
            q = (query[word] * idfWord[word])
            queryN += math.pow(q,2)
            
            
            
        return math.sqrt(queryN)


        
        
    def sortDic(self, dic):
        sortedx =  sorted(dic.items(), key=itemgetter(1), reverse=True)[:10]
      
        return sortedx
    def getCollectionSize(self):
        maxID = 0
        for word in self.index:
             newID = max(self.index.get(word,1), key = self.index.get(word,1).get)
             if newID > maxID:
                 maxID = newID
            
      
        return maxID


       

       
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
            
    def termFreqIDF(self,currentDoc, query, idfWord, qDocs):
        termFreqIDF = 0
        normDoc = 0
        for word in query:
            if word in qDocs[currentDoc]:
                wordTfIdf = qDocs[currentDoc][word] * idfWord[word]
                normDoc += math.pow(wordTfIdf,2)
                termFreqIDF += wordTfIdf
      
        return (termFreqIDF, math.sqrt(normDoc))