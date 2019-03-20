import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client.yelp
collection = db.business

db.business.create_index([('name', 'text')])

def search_business_name(query):
    results = db.business.find({'name': query})
    result_count = db.business.find({'name': query}).count()
    return results, result_count