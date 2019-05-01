import pymongo

client = pymongo.MongoClient('localhost', 27017)
db = client.yelp
collection = db.business

#Must create index to be able to search text
db.business.create_index([('name', 'text')])

def search_business_name(search):
    results = db.business.find({'$text': {'$search': search}})
    return results

def search_business_count(search):
    result_count = db.business.find({'$text': {'$search': search}}).count()
    return result_count

def random_restaurant():
    random_results = db.business.aggregate(
        [{'$sample': {'size': 1}}]
    )
    return random_results
