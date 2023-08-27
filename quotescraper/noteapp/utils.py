from pymongo import MongoClient


def get_mongodb():
    """
    The get_mongodb function connects to the MongoDB database and returns a reference to it.
    
    :return: The database object
    :doc-author: Trelent
    """
    client = MongoClient('mongodb://localhost')

    db = client.quotescraper
    return db
