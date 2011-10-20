# -*- coding: utf-8 -*-

"""
document needs to be sorted by user
"""


__author__ = 'Christian Körner'

import os
import lucene
import logging
import math

from lucene import Version, Document, SimpleFSDirectory, Term

FORMAT = '%(asctime)-15s %(funcName)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('tagging_analysis')
logger.setLevel(logging.WARNING)


from tagging.tagger_analysis import tagger_analysis

class LuceneIndexer:
    """
    Class for Lucene Indexing
    """

    def __init__(self, indexDir, analyzer):
        """
        Constructor
        """
        if not os.path.exists(indexDir):
            os.mkdir(indexDir)

        self.indexdir_ = indexDir
        store = SimpleFSDirectory(lucene.File(indexDir))
        self.writer = lucene.IndexWriter(store, analyzer, True, lucene.IndexWriter.MaxFieldLength.LIMITED, create=True)
        self.writer.setMaxFieldLength(1048576)
        self.global_occs = {}

    def optimize_and_close(self):
        """
        optimizes and closes the index
        """
        self.writer.optimize()
        self.writer.close()


    def index_user(self, user):
        """
        indexes a user
        """
        #print user.name

        tag_string = ""

        #logger.info("indexing user %s", user.name)

        for tag, occ in user.get_tags_and_occurrences().iteritems():

            try:
                self.global_occs[unicode(tag)] += occ
            except KeyError:
                self.global_occs[unicode(tag)] = occ

            tag_string += (tag + " ") * occ

        doc = lucene.Document()
        doc.add(lucene.Field("name", user.name, lucene.Field.Store.YES, lucene.Field.Index.NOT_ANALYZED))
        doc.add(lucene.Field("tags", tag_string, lucene.Field.Store.YES, lucene.Field.Index.ANALYZED))


        self.writer.addDocument(doc)

    def computeTFIDF(self):
        """
        computes tfidf for all terms globally
        """
        fsDir = lucene.SimpleFSDirectory(lucene.File(self.indexdir_))
        reader = lucene.IndexReader.open(fsDir)

        numDocs = float(reader.numDocs())

        terms = reader.terms(Term("tags"))

        key_errors = 0

        while terms.next():
            x = terms.term()

            docFreq = reader.docFreq(x)

            try:
                print "%s\t%s" % (x.text(), self.global_occs[x.text()] *  math.log(numDocs / (1.0 + float(docFreq))))
            except KeyError:
                logger.warning("could not find tag %s in global tag lookup" % x.text())
                key_errors += 1
                continue
        logger.info("%s KeyErrors in the lookup" % key_errors)
        
        reader.close()



def lucene_experiment():
    """
    A lucene experiment
    """

    logger.info("starting experiment")

    lucene.initVM()
    lucene_indexer = LuceneIndexer("index", lucene.WhitespaceAnalyzer(Version.LUCENE_CURRENT))
    tagger_analysis(analysis_function=lucene_indexer.index_user)
    logging.info("done reading users")
    lucene_indexer.optimize_and_close()
    lucene_indexer.computeTFIDF()


if __name__ == "__main__":
    lucene_experiment()