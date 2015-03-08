from mongoengine import *
from django.core.urlresolvers import reverse


class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)


# class Review(EmbeddedDocument):
class Review(Document):
    # user = ReferenceField(User, reverse_delete_rule=CASCADE)
    title = StringField(max_length=200, required=True)
    text = StringField(required=True)
    tags = ListField(StringField(max_length=30))
    rating = IntField(min_value=1, max_value=5)
    store_id = StringField()


    def get_store_id(self, store_id):
        self.store_id = store_id
        return store_id

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        return super(Review,
                     self).save()  #title=self.title, text=self.text, tags=self.tags, rating=self.rating, store_id=self.store_id)

    def get_absolute_url(self):
        return reverse('review_detail', args=[self.id])

    def get_edit_url(self):
        return reverse('review_update', args=[self.id])

    def get_delete_url(self):
        return reverse('review_delete', args=[self.id])


class Tags(EmbeddedDocument):
    content = StringField()


class Store(Document):
    # user = ReferenceField(User, reverse_delete_rule=CASCADE)
    name = StringField(max_length=200, required=True)
    description = StringField(required=True)
    address1 = StringField(required=True)
    address2 = StringField()
    city = StringField(required=True)
    state = StringField(required=True)
    zipcode = IntField()
    latitude = StringField()
    longitude = StringField()
    # text_length = IntField()
    #date_modified = DateTimeField(default=datetime.now)
    tags = ListField(EmbeddedDocumentField(Tags))
    #reviews = ListField(EmbeddedDocumentField(Review))

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # self.text_length = len(self.text)
        return super(Store, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail', args=[self.id])

    def get_edit_url(self):
        return reverse('update', args=[self.id])

    def get_delete_url(self):
        return reverse('delete', args=[self.id])