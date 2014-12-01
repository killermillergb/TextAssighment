from __future__ import division
from operator import itemgetter

import math
##I have brought up the Main Classes which carry out the main operation 
##to help improve readblity of my code  

#I was a little unsure about what was expect of the binary so i just return
#ten docs which contain one of the terms
#I had a different Binary version which took into account of how many of the
#terms were found in the doc. But binary is it found Yes OR No, so i have left
#what i think is right.

#I have kept the code commented incase i was right i was meant to take into 
#account how many times the word is found
class Binary:
    def __init__(self,qDoc):
#        self.qDocs = {}        
#        for docIDs in docList:
#            self.qDocs[docIDs]=0
#        for word in query:
#            #if the word is not in index catch error
#            if word in index:            
#                for wordDocID in index[word]:
#                        self.qDocs[wordDocID] += 1
        
        
        #if a term has been found then add it to the array
        self.bDoc = []
        for docID in qDoc:
            self.bDoc.append(docID)
            
    #return 10 of the docs found
    def getResults(self):
        return self.bDoc[:10]
            
#As stated in the assighment, it works out the TermFrequency for each doc
#and returns the results to be sorted later
class TF:
    def __init__(self, index, qDocs, query):
        self.tf= {}
#Since i have already restructed the Index to a DocID{ Words {count}} all i had
#to do was to sum each doc, then return the results to be sorted later 
        for docID in qDocs:
             self.tf[docID] = sum(qDocs[docID].itervalues())
#returns results
    def getTF(self):
        return self.tf


#Words out the Cos(query,Doc)
#The code is very compacted to from the removal of wasted index looping
#This has resulted in the code running alot faster but hopfully still looks
#neat enough for others to read.

#I have tried to follow the notes as close as possible to the assighment, so 
#I only loop through the Index once.
class TFIDF:
    #init class aswell working the IDF for the words relvant to query
    def __init__(self, sizeOfCollection, query, index):
        #Declar some dataStructures
        self.idfWord = {}
        self.normalized = {}
        self.query = query
        self.index = index
        #The only index loop
        for word in index:
            #works out how how many documents contain the word in question
             documentFreq = len(index.get(word,1))
             #Carries out the IDF for the current word
             self.idfWord[word] = math.log10(float(sizeOfCollection)/float(documentFreq))
             #for every document which contains the word in question and  how many times
             # the word occures  times by the IDF vaule then square and store for normalization
             for docID in self.index[word]:
               #  if word in qDocs[currentDoc]:
                 
                 if docID in  self.normalized:
                     self.normalized[docID] += (self.index[word][docID]*self.idfWord[word])**2
                 else:
                     self.normalized[docID] = (self.index[word][docID]*self.idfWord[word])**2
        #Perform Normalization for each document
        for doc in self.normalized:
             self.normalized[doc] =math.sqrt(self.normalized[doc])
                     
               
               
               
    #Works out the TFIDF
    #Since i have removed all pointless index looping i perform dictionary look ups to
    #word out the TFIDF. Which is the TF times the IDF for doc and query followed by taken
    #the nomalization into account
    def termFreqIDF(self,currentDoc, qDocs):
        termFreqIDF = 0
        
        
        for word in self.query:
            if word in qDocs[currentDoc]:
                #Works out the TFIDF for the word in the Document
                wordTfIdf = qDocs[currentDoc][word] * self.idfWord[word] 
                #Works out the TFIF for the terms in the query
                queryScore = self.query[word]*self.idfWord[word]                
                
                #Works out the Cos(D,Q),ie the TFIDF(DQ)/norm(D)
                #Times the Doc score by the query score followed by dividing it by
                #the norm
                termFreqIDF += (wordTfIdf * queryScore)/self.normalized[currentDoc]
        #returns the result for the Document in question
        return termFreqIDF

#I perform a switch statment to swtich between Binary, TF and TFIDF
class Retrieve:
    def __init__(self,index,termWeighting):
        self.index = index
        self.termWeighting = termWeighting

    def forQuery(self,query):
      
        #Creates a new index but based on DocID which contains dic of words and
        #how many times the word occources in the document.
        #Also it only brings back document were atleast one of the terms were found
      
      #The Data structure allows for a quick look up to into a Document which is
      #very usful for when coming to a TFIDF
        qDocs = self.findDocs(query)
        
        scoreOfDoc = {}
        #gets the binary score
        if(self.termWeighting == 'binary'):
            binary = Binary(qDocs)
            #returns the score
            return binary.getResults()
        #gets the TF score
        elif(self.termWeighting == 'tf'):
           
                tf = TF(self.index, qDocs, query)
                #returns the score
                return self.sortDic(tf.getTF())
              
        #gets the TFIDF score
        elif(self.termWeighting == 'tfidf'):
            #gets the size of the Collection
            collectionSize = self.getCollectionSize()
            #Works out the norm and TFIDF for each word and document            
            tfidf =TFIDF(collectionSize, query,self.index)
            for doc in qDocs:
                #performs the Cos(D,Q), i have called it termFreqIDF for 
                #helping me to undertsand my code.
                scoreOfDoc[doc] = tfidf.termFreqIDF(doc, qDocs)

        #returns the score
        return self.sortDic(scoreOfDoc)
##pulls out all relvant docs into a new index by DocID, to help perform reccusive 
#steps without the need of having to reloop the index to find the DocID
        
#The you DataStucture is done by DocID{word{count}},allows for the quick look up
        
# i have also not performed a loop on the index, this makes this function very 
#effcient in extracting usful data.
    def findDocs(self,query):
        qDocs = {}
        for word in query:
            if word in self.index:
                #for every DocID for every word in the Index which is in the query
                #add to the qDoc.
                for docid in self.index[word]:
                    if docid in qDocs:
                        qDocs[docid][word] = self.index[word][docid]
                    else:
                        qDocs[docid]= {}
                        qDocs[docid][word] = self.index[word][docid]

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
            
       
        return sortedToArray



