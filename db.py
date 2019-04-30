import pymongo
# Setup
client = pymongo.MongoClient('localhost', 27017)
db = client.yelp
collection = db.business
collection2 = db.photos
# Create index on name field
# Must create index to be able to search text
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
    if q5 is not None:
        search_string.update({'stars': {'$gte': q5}})
    results = db.business.find(search_string)
    result_count = db.business.count_documents(search_string)
    return results, result_count


def display_info(d1, d2, d3, d4):
    display_string = {}
    if d1 != '':
        display_string.update({'$text': {'$search': d1}})
    if d2 != '':
        display_string.update({'hours': {'$regex': d2, '$options': 'i'}})
    if d3 != '':
        display_string.update({'latitude': {'$regex': d3, '$options': 'i'}})
    if d4 != '':
        display_string.update({'longitude': {'$regex': d4, '$options': 'i'}})
    results = db.business.find(display_string)
    result_count = db.business.display_documents(display_string)
    return results, result_count


# Funtions for sorting results
def sort_by_name(results, reverse):
    if reverse is True:
        return results.sort('name')
    else:
        return results.sort('name', -1)


def sort_by_city(results, reverse):
    if reverse is True:
        return results.sort('city')
    else:
        return results.sort('city', -1)


def sort_by_state(results, reverse):
    if reverse is True:
        return results.sort('state')
    else:
        return results.sort('state', -1)


def sort_by_stars(results, reverse):
    if reverse is True:
        return results.sort('stars')
    else:
        return results.sort('stars', -1)


def sort_by_review_count(results, reverse):
    if reverse is True:
        return results.sort('review_count')
    else:
        return results.sort('review_count', -1)


def sort_request(request, results, reverse):
    if (request == 'Name'):
        return sort_by_name(results, reverse)
    elif (request == 'City'):
        return sort_by_city(results, reverse)
    elif (request == 'State'):
        return sort_by_state(results, reverse)
    elif (request == 'Stars'):
        return sort_by_stars(results, reverse)
    elif (request == 'Reviews'):
        return sort_by_review_count(results, reverse)
    else:
        return None


# Given results of a query,
# will return a list of business_id strings and index keys
def create_business_id_list(results):
    business_ids = []
    if results is not None:
        for document in results:
            business_id = document.get('business_id')
            print(business_id)
            business_ids.append(business_id)
        results.rewind() #Rewinds the cursor back to the first document
    return business_ids


# Will query the pictures collection using the array of
# business_ids, then return a dictionary of business_ids
# and their photo_id values
def create_photo_id_dictionary(results):
    photo_dict = {}
    business_ids = create_business_id_list(results)
    #Queries the photos collection.
    photo_results = db.photos.find({'business_id': {'$in': business_ids}})
    #Convert cursor into a list of dictionaries(or Documents)
    for business_id in business_ids:


    return photo_dict
