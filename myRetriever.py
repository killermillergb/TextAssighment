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
          
        
        
        qDocs = self.findTermsDoc(query, docList)
        self.inverseDocumentFrequency(docList, qDocs, query)
        docrank =  self.sortDic(qDocs)
        
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
    def inverseDocumentFrequency(self, docList, qDocs, query):
        sizeOfCollection = len(docList)
        
        documentFreq = {}
        collectionFreq = {}
        idfWord = {}
        tfIdfWord= {}
        #add words to dic
        for word in query:
            documentFreq[word]=0
            collectionFreq[word]=0
            idfWord[word]=0
            tfIdfWord[word]=0
            
        #idf on docs inspectign, does not give rigth results so going
        #to do a idf on the whole collection.
#        for word in query:       
#           
#            for docID in docList:
#                if word in qDocs.get(docID,1):
#                    collectionFreq[word] +=  qDocs[docID][word]
#                    documentFreq[word] += 1 
            
        for word in query:
             if word in self.index:
                 wordDocIDs = self.index.get(word,1)
                 
                 documentFreq[word] = len(wordDocIDs)
                 for wordDocID in wordDocIDs:
                     collectionFreq[word] += wordDocIDs[wordDocID]
        for word in query:
            if documentFreq[word] == 0:
                idfWord[word] = 0
            else:
                idfWord[word] = math.log10(sizeOfCollection/documentFreq[word])
        
        ######
        
        #put this in a new function since this is to find what it is for the
        #current document
        #finding the term Frequency * idf
        for word in query:
            for doc in qDocs:
                currentDoc = qDocs[doc]
                if word in currentDoc:
                    tfIdfWord[word] = currentDoc[word] * idfWord[word]
                else:
                    tfIdfWord[word] = 0
        print tfIdfWord
#########                    
        
 
 
                   
                    
                        
            
            
        
        
        
        
        
        return 0
        
    def sortDic(self, dic):
        sortedx =  sorted(dic.items(), key=itemgetter(0), reverse=True)[:10]
      
        return sortedx
        

      
       
       

       
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
        