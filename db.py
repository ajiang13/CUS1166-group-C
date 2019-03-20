import pymongo
#Setup
client = pymongo.MongoClient('localhost', 27017)
db = client.yelp
collection = db.business

#Create index on name field
#Must create index to be able to search text
db.business.create_index([('name', 'text')])

#Search for businesses by name (keyword search with ORs between terms)
#Returns all matching documents
def search_business_name(search):
    results = db.business.find({'$text': {'$search': search}})
    return results
#Returns the number of documents found
def search_business_count(search):
    result_count = db.business.find({'$text': {'$search': search}}).count()
    return result_count

def search_city(search):
    results = db.business.find({'city': {'$regex': search, '$options': 'i'}})
    return results

def search_city_count(search):
    result_count = db.business.find({'city': {'$regex': search, '$options': 'i'}}).count()
    return result_count

def search_state(search):
    results = db.business.find({'state': {'$regex': search, '$options': 'i'}})
    return results

def search_state_count(search):
    result_count = db.business.find({'state': {'$regex': search, '$options': 'i'}}).count()
    return result_count

def search_stars(stars):
    results = db.business.find({'stars': {'$gte': stars}})
    return results

def search_stars_count(stars):
    result_count = db.business.find({'stars': {'$gte': stars}}).count()
    return result_count

def search_categories(search):
    results = db.business.find({'categories': {'$regex': search, '$options': 'i'}})
    return results

def search_categories_count(search):
    result_count = db.business.find({'categories': {'$regex': search, '$options': 'i'}}).count()
    return result_count
