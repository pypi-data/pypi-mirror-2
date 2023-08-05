#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Radim Rehurek <radimrehurek@seznam.cz>
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""
This module contains functions and classes for similarities across
a corpus of documents in the Vector Space Model.

The documents are sparse vectors coming from the TF-IDF model, LSI model, LDA model etc.

The two main classes are :

1. `Similarity` -- computes similarity by linearly scanning over the corpus (slower,
 memory independent)
2. `SparseMatrixSimilarity` -- stores the whole corpus in memory, computes similarity 
 by in-memory matrix-vector multiplication. This is much faster than the general 
 Similarity, so use this when dealing with smaller corpora, that fit in RAM.

Once the similarity object has been initialized, you can query for document
similarity simply by
 
>>> similarities = similarity_object[query_vector]

or iterate over within-corpus similarities with

>>> for similarities in similarity_object:
>>>     ...

-------
"""


import logging

import numpy
import scipy.sparse

from gensim import interfaces, utils, matutils



class Similarity(interfaces.SimilarityABC):
    """
    Compute cosine similary against a corpus of documents. This is done by a full 
    sequential scan of the corpus. 
    
    If your corpus is reasonably small (fits in RAM), consider using `SparseMatrixSimilarity` 
    instead of `Similarity`, for (much) faster similarity searches.
    """
    def __init__(self, corpus, numBest = None):
        """
        If `numBest` is left unspecified, similarity queries return a full list (one 
        float for every document in the corpus, including the query document).
        
        If `numBest` is set, queries return `numBest` most similar documents, as a 
        sorted list, eg. [(docIndex1, 1.0), (docIndex2, 0.95), ..., (docIndexnumBest, 0.45)].
        """
        self.corpus = corpus
        self.numBest = numBest
        self.normalize = True
    
    
    def getSimilarities(self, doc):
        return [matutils.cossim(doc, other) for other in self.corpus]
#endclass Similarity    



class SparseMatrixSimilarity(interfaces.SimilarityABC):
    """
    Compute similarity against a corpus of documents by storing its sparse 
    term-document (or concept-document) matrix in memory. The similarity measure 
    used is cosine between two vectors.
    
    This allows for faster similarity searches (simple sparse matrix-vector multiplication),
    but loses the memory-independence of an iterative corpus.

    The matrix is internally stored as a `scipy.sparse.csr` matrix.
    """
    def __init__(self, corpus, numBest = None, dtype = numpy.float32):
        """
        If `numBest` is left unspecified, similarity queries return a full list (one 
        float for every document in the corpus, including the query document):
        
        If `numBest` is set, queries return `numBest` most similar documents, as a 
        sorted list:
        
        >>> sms = SparseMatrixSimilarity(corpus, numBest = 3)
        >>> sms[vec12]
        [(12, 1.0), (30, 0.95), (5, 0.45)]
        
        """
        logging.info("creating sparse matrix for %i documents" % len(corpus))
        self.numBest = numBest
        self.corpus = scipy.sparse.lil_matrix((len(corpus), 1), dtype = dtype) # set no of columns to 1 for now, as the number of terms is unknown yet
        self.normalize = True
        
        # iterate over the corpus, populating the sparse matrix
        for docNo, vector in enumerate(corpus):
            if docNo % 10000 == 0:
                logging.info("PROGRESS: at document #%i/%i" % (docNo, len(corpus)))
            vector = matutils.unitVec(vector) # make all vectors unit length, so that cosine similarity = simple dot product
            self.corpus.rows[docNo] = [termId for termId, _ in vector]
            self.corpus.data[docNo] = [dtype(val) for _, val in vector]
        
        # now set the shape properly, using no. columns = highest term index in the corpus + 1
        numTerms = 1 + max(max(row + [-1]) for row in self.corpus.rows) # + [-1] to avoid exceptions from max(empty)
        self.corpus._shape = (len(corpus), numTerms)
        
        # convert to Compressed Sparse Row for efficient row slicing and multiplications
        self.corpus = self.corpus.tocsr()
        logging.info("created %s" % repr(self.corpus))
    
    
    def getSimilarities(self, doc):
        """
        Return similarity of sparse vector `doc` to all documents in the corpus.
        
        `doc` may be either a bag-of-words iterable (standard corpus document), 
        or a numpy array, or a `scipy.sparse` matrix. It is assumed to be of unit length.
        """
        if scipy.sparse.issparse(doc):
            vec = doc.T
        elif isinstance(doc, numpy.ndarray):
            vec = scipy.sparse.csr_matrix(doc).T # Tx1 array
        else:
            vec = scipy.sparse.dok_matrix((self.corpus.shape[1], 1), dtype = self.corpus.dtype)
            for fieldId, fieldValue in doc:
                vec[fieldId, 0] = fieldValue
        if vec.shape != (self.corpus.shape[1], 1):
            raise ValueError("vector shape mismatch; expected %s, got %s" % 
                             ((self.corpus.shape[1], 1,), vec.shape))
        
        # compute cosine similarity against every other document in the collection
        allSims = self.corpus * vec.tocsc() # N x T * T x 1 = N x 1
        allSims = list(allSims.toarray().flat) # convert to plain python list
        assert len(allSims) == self.corpus.shape[0] # make sure no document got lost!
        return allSims
#endclass SparseMatrixSimilarity

