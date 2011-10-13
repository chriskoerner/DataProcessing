# -*- coding: utf-8 -*-

"""
document needs to be sorted by user
"""


__author__ = 'Christian Körner'

import os
import lucene

from lucene import Version, Document



from tagger_analysis import tagger_analysis

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

        store = lucene.SimpleFSDirectory(lucene.File(indexDir))
        self.writer = lucene.IndexWriter(store, analyzer, True, lucene.IndexWriter.MaxFieldLength.LIMITED, create=True)
        self.writer.setMaxFieldLength(1048576)

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
        print user.name

        tag_string = ""

        for tag, occ in user.get_tags_and_occurrences().iteritems():
            tag_string += (tag + " ") * occ

        doc = lucene.Document()
        doc.add(lucene.Field("name", user.name, lucene.Field.Store.YES, lucene.Field.Index.NOT_ANALYZED))
        doc.add(lucene.Field("name", tag_string, lucene.Field.Store.YES, lucene.Field.Index.ANALYZED))

        self.writer.addDocument(doc)
        

        




def lucene_experiment():
    """
    A lucene experiment
    """
    lucene.initVM()
    lucene_indexer = LuceneIndexer("index", lucene.StandardAnalyzer(Version.LUCENE_CURRENT))
    tagger_analysis(analysis_function=lucene_indexer.index_user)

    lucene_indexer.optimize_and_close()


if __name__ == "__main__":
    lucene_experiment()