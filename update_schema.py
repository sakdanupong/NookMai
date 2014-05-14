import os,sys
sys.path.append(os.path.abspath('models'))
import logging
from moviemodel import *
from google.appengine.ext import deferred
from google.appengine.ext import db
from search_util import *


BATCH_SIZE = 100  # ideal batch size may vary based on entity size.

def UpdateSchema(cursor=None, num_updated=0):
    # delete_all_in_index(MOVIE_SEARCH_INDEX)
    query = MovieModel.all()
    if cursor:
        query.with_cursor(cursor)

    to_put = []
    for p in query.fetch(limit=BATCH_SIZE):
        # In this example, the default values of 0 for num_votes and avg_rating
        # are acceptable, so we don't need this loop.  If we wanted to manually
        # manipulate property values, it might go something like this:
        # if p.rate_count is None or p.rate_count == 0:
        #     p.rate_count = 10
        #     to_put.append(p)
        createMovieTextSearchDoc(p.id, p.search_tag)


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