import datetime
import time

from bookreader.models import Book
from bookreader.harvesting.metadata import metadata_registry
from bookreader.harvesting.book import load_metadata

def load_books(collection, **kwargs):
    kw = {}
    kwargs.setdefault('metadataPrefix', 'dim')
    
    if 'metadata_registry' in kwargs:
        kw['metadata_registry'] = kwargs.pop('metadata_registry')
    else:
        kw['metadata_registry'] = metadata_registry
    
    repo = collection.repository.connection(**kw)
    
    loaded = 0
    skipped = 0
    
    load_kw = kw.copy()
    load_kw.update(kwargs)
    
    for header in repo.getItemIdentifiers(collection=collection.handle, **kwargs):
        try:
            book = Book.objects.get(identifier=header.identifier())
        except Book.DoesNotExist:
            book = Book(identifier=header.identifier(), collection=collection)
            book.save()
            loaded += 1
        else:
            skipped += 1
            continue
    
    return (loaded, skipped,)
    