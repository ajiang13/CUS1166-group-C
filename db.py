import pymongo
import json
#Setup
client = pymongo.MongoClient('localhost', 27017)
db = client.yelp
collection = db.business
collection2 = db.pictures

#Create index on name field
#Must create index to be able to search text
db.business.create_index([('name', 'text')])

def advanced_search(q1, q2, q3, q4, q5):
    search_string = {}
    if q1 != '':
        search_string.update({'$text': {'$search': q1}})
    if q2 != '':
        search_string.update({'city': {'$regex': q2, '$options': 'i'}})
    if q3 != '':
        search_string.update({'state': {'$regex': q3, '$options': 'i'}})
    if q4 != '':
        search_string.update({'categories': {'$regex': q4, '$options': 'i'}})
    if q5 != None:
        search_string.update({'stars': {'$gte': q5}})
    results = db.business.find(search_string)
    result_count = db.business.count_documents(search_string)
    return results, result_count

#Funtions for sorting results
def sort_by_name(results,reverse):
    if (reverse == True):
        return results.sort('name')
    else:
        return results.sort('name',-1)

def sort_by_city(results,reverse):
    if (reverse == True):
        return results.sort('city')
    else:
        return results.sort('city',-1)

def sort_by_state(results,reverse):
    if (reverse == True):
        return results.sort('state')
    else:
        return results.sort('state',-1)

def sort_by_stars(results,reverse):
    if (reverse == True):
        return results.sort('stars')
    else:
        return results.sort('stars', -1)

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

#Given results of a query,
#will return a Dict of photo_id values and their
#corresponding business_id keys
def photo_results(results):
    picture_results = {}
    if results != None:
        for document in results:
            doc_id = document.get('business_id')
            #picture_doc isn't the same type as document??
            #try just using pymongo api functions since we're dealing w cursor objects,
            #it might help with avoiding problem on line 82
            picture_doc = db.pictures.find_one({'business_id', doc_id})
            picture_results[doc_id] = picture_doc.get('photo_id')
    return picture_results

#Returns a single photo_id
def find_photo_url(document, results):
    pictures = photo_results(results)
    for pic in pictures:
        if document.business_id == pic.business_id:
            return pic.photo_id

#Returns a dictionary of picture file names for the passed results
def find_photo_urls(results):
    pictures = photo_results(results)
    picture_urls = {}
    for picture in pictures:
        picture_urls[picture.business_id] = picture.photo_id
    return picture_urls
