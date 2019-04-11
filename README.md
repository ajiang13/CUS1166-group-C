# CUS1166 project: <a href=https://www.yelp.com/>Yelp</a>-like app in Flask
CUS1166 group C

Setup requires importing data into MongoDB. Download from: https://www.yelp.com/dataset/download

Relevant files: yelp_dataset.tar.gz (business.json, review.json, photo.json), yelp_photos.tar.gz (photos).

### MongoDB setup:

1. <a href=https://www.mongodb.com/download-center/community>Download MongoDB</a> and install (with Compass).
2. Connect to server (localhost:27017) - easy via Compass.
3. Create 'yelp' database - easy via Compass.
4. Create 'business' and 'photo' collections - easy via Compass.

Import data from .json files:

5. Open command prompt (not Mongo Shell) and change directory to MongoDB installation e.g. `cd C:\Program Files\MongoDB\Server\4.0\bin`
6. Enter `mongoimport --db yelp --collection business --file <path to business.json>` and again for the photo collection.

If successful, the business collection should have 192.6k documents and 200.0k photo documents.
