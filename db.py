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

def advanced_search(search):
    results = db.business.find(search)
    return results

def advanced_search_count(search):
    result_count = db.business.find(search)
    return result_count

#Funtions for sorting results
def sort_by_name(results,reverse):
    if (reverse == True):
        return results.sort('name', -1)
    else:
        return results.sort('name')

def sort_by_city(results,reverse):
    if (reverse == True):
        return results.sort('city', -1)
    else:
        return results.sort('city')

def sort_by_state(results,reverse):
    if (reverse == True):
        return results.sort('state', -1)
    else:
        return results.sort('state')

#We want businesses with more stars to
#appear first, so the sort is flipped
def sort_by_stars(results,reverse):
    if (reverse == True):
        return results.sort('stars')
    else:
        return results.sort('stars', -1)

#This sort is also flipped compared to the others
def sort_by_review_count(results,reverse):
    if (reverse == True):
        return results.sort('review_count')
    else:
        return results.sort('review_count', -1)

def sort_request(request,results,reverse):
    if (request == 'Name'):
        return sort_by_name(results,reverse)
    elif (request == 'City'):
        return sort_by_city(results,reverse)
    elif (request == 'State'):
        return sort_by_state(results,reverse)
    elif (request == 'Stars'):
        return sort_by_stars(results,reverse)
    elif (request == 'Reviews'):
        return sort_by_review_count(results,reverse)
    else:
        return None
