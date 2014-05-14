MOVIE_SEARCH_INDEX = 'MOVIE_SEARCH_INDEX'
from google.appengine.api import search

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

def createMovieTextSearchDoc(c_id, arr_text):
    index = search.Index(name=MOVIE_SEARCH_INDEX)
    doc_id = str(c_id)
    name = ','.join(arr_text)
    document = search.Document(
            doc_id=doc_id,
            fields=[search.TextField(name='name', value=name)])
    index.put(document)


def delete_all_in_index(index_name):
    """Delete all the docs in the given index."""
    doc_index = search.Index(name=index_name)

    # looping because get_range by default returns up to 100 documents at a time
    while True:
        # Get a list of documents populating only the doc_id field and extract the ids.
        document_ids = [document.doc_id
                        for document in doc_index.get_range(ids_only=True)]
        if not document_ids:
            break
        # Delete the documents for the given ids from the Index.
        doc_index.delete(document_ids)