import pymongo
#Setup
client = pymongo.MongoClient('localhost', 27017)
db = client.yelp
collection = db.business

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

def filter_by_stars(results,stars):
    #We want to include documents with the entered num of stars
    #while excluding results below that number
    stars = stars - .1
    star_results = db.business.find({'stars': {'$gt':stars}})
    #Need to merge results and star_results and return the common documents
    return results
