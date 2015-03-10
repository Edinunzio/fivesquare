from datetime import datetime

from pymongo import Connection, GEO2D

from mongoengine import *
from django.core.urlresolvers import reverse


class GeoIndex(Document):
    def insert_store_by_location(self, db, stores):
        db = Connection().geo_stores
        db.places.create_index([("loc", GEO2D)])
        for store in stores:
            db.places.insert({"loc": [store['longitude'], store['latitude']],
                              "store_info": {"id": store['id'], "name": store["name"], "address": store["address1"],
                                             "city": store["city"], "state": store["state"],
                                             "zipcode": store["zipcode"]}})

    def filter_by_point(self, db, longitude, latitude, lm):
        results = []
        for doc in db.places.find({"loc": {"$near": [longitude, latitude]}}).limit(lm):
            repr(doc)
            results.append(doc)
        return results


class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


class Review(Document):
    title = StringField(max_length=200, required=True)
    text = StringField(required=True)
    tags = ListField(StringField(max_length=30))
    rating = IntField(min_value=1, max_value=5)
    date_modified = DateTimeField(default=datetime.now)
    store_id = StringField()

    def get_store_id(self, store_id):
        self.store_id = store_id
        return store_id

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        return super(Review,
                     self).save()

    def get_absolute_url(self):
        return reverse('review_detail', args=[self.id])

    def get_edit_url(self):
        return reverse('review_update', args=[self.id])

    def get_delete_url(self):
        return reverse('review_delete', args=[self.id])


class Location(Document):
    point = PointField()


class Store(Document):
    name = StringField(max_length=200, required=True)
    description = StringField(required=True)
    address1 = StringField(required=True)
    city = StringField(required=True)
    state = StringField(required=True)
    zipcode = IntField()
    latitude = FloatField()
    longitude = FloatField()
    loc = PointField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        return super(Store, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail', args=[self.id])

    def get_edit_url(self):
        return reverse('update', args=[self.id])

    def get_delete_url(self):
        return reverse('delete', args=[self.id])