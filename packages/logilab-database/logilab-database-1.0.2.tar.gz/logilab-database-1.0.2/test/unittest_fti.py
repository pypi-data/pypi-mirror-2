# -*- coding: iso-8859-1 -*-
import unittest

from logilab.common.testlib import MockConnection

from logilab.database.fti import FTIndexerMixIn, tokenize, normalize

def _tokenize(string):
    words = []
    for word in tokenize(string):
        try:
            words.append(normalize(word))
        except StopWord:
            continue
    return words

class TokenizeTC(unittest.TestCase):

    def test_utf8(self):
        self.assertEquals(_tokenize(u'n�2'),
                          ['n2'])


class IndexableObject:
    def get_words(self):
        return tokenize(u'g�nco-jpl bl� bl�p bl�p bl�p')


class IndexerTC(unittest.TestCase):

    def setUp(self):
        self.cnx = MockConnection( ([1, 2],) )
        self.indexer = FTIndexerMixIn()
        self.indexer._cnx = self.cnx
        #Indexer('sqlite', self.cnx)

    def test_index_object(self):
        self.indexer.index_object(1, IndexableObject())
        self.assertEquals(self.cnx.received,
                          [('SELECT word_id FROM word WHERE word=%(word)s;', {'word': 'ginco'}),
                           ('INSERT INTO appears(uid, word_id, pos) VALUES (%(uid)s,%(wid)s,%(position)s);', {'position': 0, 'wid': 1, 'uid': 1}),
                           ('SELECT word_id FROM word WHERE word=%(word)s;', {'word': 'jpl'}),
                           ('INSERT INTO appears(uid, word_id, pos) VALUES (%(uid)s,%(wid)s,%(position)s);', {'position': 1, 'wid': 1, 'uid': 1}),
                           ('SELECT word_id FROM word WHERE word=%(word)s;', {'word': 'bla'}),
                           ('INSERT INTO appears(uid, word_id, pos) VALUES (%(uid)s,%(wid)s,%(position)s);', {'position': 2, 'wid': 1, 'uid': 1}),
                           ('SELECT word_id FROM word WHERE word=%(word)s;', {'word': 'blip'}),
                           ('INSERT INTO appears(uid, word_id, pos) VALUES (%(uid)s,%(wid)s,%(position)s);', {'position': 3, 'wid': 1, 'uid': 1}),
                           ('SELECT word_id FROM word WHERE word=%(word)s;', {'word': 'blop'}),
                           ('INSERT INTO appears(uid, word_id, pos) VALUES (%(uid)s,%(wid)s,%(position)s);', {'position': 4, 'wid': 1, 'uid': 1}),
                           ('SELECT word_id FROM word WHERE word=%(word)s;', {'word': 'blap'}),
                           ('INSERT INTO appears(uid, word_id, pos) VALUES (%(uid)s,%(wid)s,%(position)s);', {'position': 5, 'wid': 1, 'uid': 1})])

    def test_fulltext_search(self):
        list(self.indexer.fulltext_search(u'ginco'))
        self.assertEquals(self.cnx.received,
                          [('SELECT count(*) as rating, appears0.uid FROM appears as appears0, word as word0 WHERE word0.word = %(word0)s  AND word0.word_id = appears0.word_id  GROUP BY appears0.uid ;',
                            {'word0': 'ginco'})
                           ])

    def test_fulltext_search2(self):
        list(self.indexer.fulltext_search(u'ginco-jpl'))
        self.assertEquals(self.cnx.received,
                          [('SELECT count(*) as rating, appears0.uid FROM appears as appears0, word as word0, appears as appears1, word as word1 WHERE word0.word = %(word0)s  AND word0.word_id = appears0.word_id  AND word1.word = %(word1)s  AND word1.word_id = appears1.word_id  AND appears0.uid = appears1.uid  GROUP BY appears0.uid ;',
                            {'word1': 'jpl', 'word0': 'ginco'})
                           ])


class GetSchemaTC(unittest.TestCase):

    def test(self):
        indexer = FTIndexerMixIn()
        indexer.sql_create_sequence = lambda x: 'CREATE SEQUENCE %s;' % x
        self.assertEquals(indexer.sql_init_fti(),
                          '''
CREATE SEQUENCE word_id_seq;

CREATE TABLE word (
  word_id INTEGER PRIMARY KEY NOT NULL,
  word    VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE appears(
  uid     INTEGER,
  word_id INTEGER REFERENCES word ON DELETE CASCADE,
  pos     INTEGER NOT NULL
);

CREATE INDEX appears_uid ON appears (uid);
CREATE INDEX appears_word_id ON appears (word_id);
''')

if __name__ == '__main__':
    unittest.main()
