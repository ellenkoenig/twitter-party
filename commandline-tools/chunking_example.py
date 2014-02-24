# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 13:23:50 2013

@author: Claudine
"""

# http://www.eecis.udel.edu/~trnka/CISC889-11S/lectures/dongqing-chunking.pdf
# examples actually taken from
# http://nltk.org/book3/ch07.html
import nltk

class ChunkParser(nltk.ChunkParserI): 
    def __init__(self, train_sents): 
        train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)] 
            for sent in train_sents] 
        self.tagger = nltk.UnigramTagger(train_data) 
 
    def parse(self, sentence): 
        pos_tags = [pos for (word,pos) in sentence] 
        tagged_pos_tags = self.tagger.tag(pos_tags) 
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags] 
        conlltags = [(word, pos, chunktag) for ((word,pos),chunktag) 
            in zip(sentence, chunktags)] 
        return nltk.chunk.util.conlltags2tree(conlltags)

# get training and testing data 
test_sents = nltk.corpus.conll2000.chunked_sents('test.txt', chunk_types=['NP']) 
train_sents = nltk.corpus.conll2000.chunked_sents('train.txt', chunk_types=['NP']) 
 
# training the chunker, ChunkParser is a class defined in the next slide 
NPChunker = ChunkParser(train_sents) 
print NPChunker.evaluate(test_sents) 
