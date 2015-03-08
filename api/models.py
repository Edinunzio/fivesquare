from datetime import datetime

from mongoengine import *
from django.core.urlresolvers import reverse


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


class Tags(EmbeddedDocument):
    content = StringField()


class Store(Document):
    name = StringField(max_length=200, required=True)
    description = StringField(required=True)
    address1 = StringField(required=True)
    city = StringField(required=True)
    state = StringField(required=True)
    zipcode = IntField()
    latitude = StringField()
    longitude = StringField()

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