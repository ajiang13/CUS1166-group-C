import pymongo
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

#Finds the corresponding doc by id in pictures collection
#Returns a new results with matching business_ids, but from pictures collection
def photo_results(results):
    picture_results = []
    for document in results:
        if db.pictures.findOne(document.business_id):
            picture_doc = db.pictures.findOne(document.business_id)
            picture_results.append(picture_doc)
    return picture_results

#Returns a single photo_id 
def find_photo_url(document, results):
    pictures = photo_results(results)
    for pic in pictures:
        if document.business_id == pic.business_id
        return pic.photo_id

#Returns a dictionary of picture file names for the passed results
def find_photo_urls(results):
    pictures = photo_results(results)
    picture_urls = {}
    for picture in pictures:
        picture_urls[picture.business_id] = picture.photo_id
    return picture_urls
