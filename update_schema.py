import logging
from moviemodel import *
from google.appengine.ext import deferred
from google.appengine.ext import db

BATCH_SIZE = 100  # ideal batch size may vary based on entity size.

def tokenize_autocomplete(phrase):
        a = []
        for word in phrase.split():
            j = 1
            while True:
                for i in range(len(word) - j + 1):
                    a.append(word[i:i + j])
                if j == len(word):
                    break
                j += 1
        return a

def createMovieTextSearchDoc(c_key, arr_text):
    index = search.Index(name=MOVIE_SEARCH_INDEX)
    doc_id = str(c_key)
    name = ','.join(arr_text)
    document = search.Document(
            doc_id=doc_id,
            fields=[search.TextField(name='name', value=name)])
    index.put(document)


def UpdateSchema(cursor=None, num_updated=0):
    query = MovieModel.all()
    if cursor:
        query.with_cursor(cursor)

    to_put = []
    for p in query.fetch(limit=BATCH_SIZE):
        # In this example, the default values of 0 for num_votes and avg_rating
        # are acceptable, so we don't need this loop.  If we wanted to manually
        # manipulate property values, it might go something like this:
        if p.search_tag is None:
            tag = tokenize_autocomplete(name_en + ' ' + name_th)
            p.search_tag = tag
            createMovieTextSearchDoc(c_key, tag)
            to_put.append(p)

    if to_put:
        db.put(to_put)
        num_updated += len(to_put)
        logging.debug(
            'Put %d entities to Datastore for a total of %d',
            len(to_put), num_updated)
        deferred.defer(
            UpdateSchema, cursor=query.cursor(), num_updated=num_updated)
    else:
        logging.debug(
            'UpdateSchema complete with %d updates!', num_updated)