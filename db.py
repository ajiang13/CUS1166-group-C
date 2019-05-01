import pymongo
import os
# Setup
MONGO_URI = os.environ.get('MONGODB_URI')
if not MONGO_URI:
    MONGO_URI = 'mongodb://localhost:27017/yelp'
client = pymongo.MongoClient(MONGO_URI)
MONGODB_NAME = os.environ.get('MONGODB_NAME')
if not MONGODB_NAME:
    MONGODB_NAME = 'yelp'
db = client[MONGODB_NAME]
print('Connecting to:')
print(db)
collection = db.business
collection2 = db.photo
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
    result_count = db.business.count(search_string)
    return results, result_count


def add_restaurant(a1, a2, a3, a4, a5, a6):
    db.business.insert_one({"name": a1,  "address": a2, "city": a3, "state": a4, "zip_code": a5, "categories": a6})


def edit_restaurant(e1, e2, e3, e4, e5, e6):
    db.business.update_one({}, {'$set': {"name": e1, "address": e2,
    "city": e3, "state": e4, "zip_code": e5, "categories": e6}}, upsert=False)


# Funtions for sorting results
def sort_by_name(results, reverse):
    if (reverse == True):
        return results.sort('name')
    else:
        return results.sort('name', -1)


def sort_by_city(results, reverse):
    if (reverse == True):
        return results.sort('city')
    else:
        return results.sort('city', -1)


def sort_by_state(results, reverse):
    if (reverse == True):
        return results.sort('state')
    else:
        return results.sort('state', -1)


def sort_by_stars(results, reverse):
    if (reverse == True):
        return results.sort('stars')
    else:
        return results.sort('stars', -1)


def sort_by_review_count(results, reverse):
    if (reverse == True):
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
# will return a dictionary of business_id strings and index keys
def create_business_id_list(results):
    business_ids = []
    if results is not None:
        for document in results:
            business_id = document.get('business_id')
            business_ids.append(business_id)
        # Rewinds the cursor back to the first document
        results.rewind()
    return business_ids


# Will query the pictures collection using the list of
# business_ids, then return a dictionary of business_ids
# and their photo_id values
def create_photo_id_dictionary(results):
    photo_dict = {}
    business_ids = create_business_id_list(results)
    for business_id in business_ids:
        try:
            # Queries the pictures collection
            photo = db.photo.find_one({'business_id': business_id})
            photo_id = photo['photo_id']
            photo_dict[business_id] = photo_id
        except:
            pass
    results.rewind()
    return photo_dict
